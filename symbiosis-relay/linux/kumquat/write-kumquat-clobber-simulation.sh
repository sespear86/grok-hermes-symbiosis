#!/usr/bin/env bash
# Bash mirror of Write-KumquatClobberSimulationEvidence — prove guard repairs harness clobber within wait window.
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=kumquat-wa-lib.sh
source "${SCRIPT_DIR}/kumquat-wa-lib.sh"

GOAL_ROOT=${1:-}
GOAL_ID=${2:-}
ATTEMPT=${3:-}
SCRATCH_DIR=${4:-}
WAIT_SECONDS=${5:-5}

if [[ -z "$GOAL_ROOT" || -z "$GOAL_ID" || -z "$ATTEMPT" || -z "$SCRATCH_DIR" ]]; then
  echo "USAGE: $0 GOAL_ROOT GOAL_ID ATTEMPT SCRATCH_DIR [WAIT_SECONDS]" >&2
  exit 2
fi

patch_out="${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch"
out_path="${SCRATCH_DIR}/kumquat-clobber-simulation.txt"
sync_script="${SCRIPT_DIR}/sync-kumquat-verifier-inputs.sh"
auth_patch="${SCRATCH_DIR}/kumquat-git-diff.patch"

{
  echo "# Kumquat clobber simulation evidence"
  echo "generated: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "patch: ${patch_out}"
  echo
} >"$out_path"

if [[ ! -f "$patch_out" ]]; then
  echo "pre_clobber: MISSING" >>"$out_path"
  echo "simulation_pass: false"
  exit 1
fi

pre_first=$(head -1 "$patch_out")
pre_size=$(wc -c <"$patch_out")
{
  echo "pre_clobber_first_line: ${pre_first}"
  echo "pre_clobber_bytes: ${pre_size}"
} >>"$out_path"

printf 'diff --git a/agent-tools/SIMULATED-CLOBBER\n' >"$patch_out"
echo "clobber_written: $(date '+%Y-%m-%d %H:%M:%S')" >>"$out_path"

deadline=$((SECONDS + WAIT_SECONDS))
repaired=false
while [[ $SECONDS -lt $deadline ]]; do
  if ! kumquat_patch_needs_repair "$patch_out"; then
    repaired=true
    break
  fi
  sleep 0.1
done

if [[ "$repaired" != true && -f "$auth_patch" ]]; then
  bash "$sync_script" "$GOAL_ROOT" "$GOAL_ID" "$ATTEMPT" "$auth_patch" "$SCRATCH_DIR" >>"$out_path" 2>&1 || true
  if ! kumquat_patch_needs_repair "$patch_out"; then
    repaired=true
  fi
fi

post_first=$(head -1 "$patch_out" 2>/dev/null || true)
post_size=0
[[ -f "$patch_out" ]] && post_size=$(wc -c <"$patch_out")
{
  echo "post_wait_first_line: ${post_first}"
  echo "post_wait_bytes: ${post_size}"
  echo "guard_repaired_within_${WAIT_SECONDS}s: ${repaired}"
  echo "simulation_pass: ${repaired}"
} >>"$out_path"

if [[ "$repaired" == true ]]; then
  echo "CLOBBER_SIMULATION_OK bytes=${post_size}"
  exit 0
fi
echo "CLOBBER_SIMULATION_FAIL" >&2
exit 1