#!/usr/bin/env bash
# Bash mirror of Invoke-KumquatVerifierPatchGuard.ps1 — detached repair loop.
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=kumquat-wa-lib.sh
source "${SCRIPT_DIR}/kumquat-wa-lib.sh"

GOAL_ROOT=${1:-}
GOAL_ID=${2:-}
ATTEMPT=${3:-}
AUTHORITATIVE_PATCH=${4:-}
SCRATCH_DIR=${5:-}
DURATION_SECONDS=${6:-600}
POLL_MS=${7:-50}

if [[ -z "$GOAL_ROOT" || -z "$GOAL_ID" || -z "$ATTEMPT" || -z "$AUTHORITATIVE_PATCH" ]]; then
  echo "USAGE: $0 GOAL_ROOT GOAL_ID ATTEMPT AUTHORITATIVE_PATCH [SCRATCH_DIR] [DURATION_SECONDS] [POLL_MS]" >&2
  exit 2
fi

patch_out="${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch"
log_path="${SCRATCH_DIR:-$GOAL_ROOT}/kumquat-patch-guard.log"
sync_script="${SCRIPT_DIR}/sync-kumquat-verifier-inputs.sh"

glog() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >>"$log_path"
}

glog "GUARD_START pid=$$ attempt=${ATTEMPT} patch=${patch_out} duration=${DURATION_SECONDS}s poll=${POLL_MS}ms"
deadline=$((SECONDS + DURATION_SECONDS))
repairs=0

while [[ $SECONDS -lt $deadline ]]; do
  if kumquat_patch_needs_repair "$patch_out"; then
    size=0
    mtime=missing
    snippet=
    if [[ -f "$patch_out" ]]; then
      size=$(wc -c <"$patch_out")
      mtime=$(stat -c '%y' "$patch_out" 2>/dev/null || stat -f '%Sm' "$patch_out")
      snippet=$(head -1 "$patch_out" 2>/dev/null || true)
    fi
    bash "$sync_script" "$GOAL_ROOT" "$GOAL_ID" "$ATTEMPT" "$AUTHORITATIVE_PATCH" "$SCRATCH_DIR" >>"$log_path" 2>&1 || true
    repairs=$((repairs + 1))
    post_size=0
    post_ok=NO
    if [[ -f "$patch_out" ]]; then
      post_size=$(wc -c <"$patch_out")
      if ! kumquat_patch_needs_repair "$patch_out"; then
        post_ok=YES
      fi
    fi
    glog "GUARD_REPAIR #${repairs} clobber_detected bytes=${size} repaired_bytes=${post_size} repair_ok=${post_ok}"
  fi
  sleep "$(awk "BEGIN {printf \"%.3f\", ${POLL_MS}/1000}")"
done

if kumquat_patch_needs_repair "$patch_out"; then
  glog "GUARD_END repairs=${repairs} final_patch_ok=false"
  exit 1
fi
glog "GUARD_END repairs=${repairs} final_patch_ok=true"