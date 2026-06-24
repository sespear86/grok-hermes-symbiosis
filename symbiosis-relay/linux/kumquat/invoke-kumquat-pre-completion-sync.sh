#!/usr/bin/env bash
# Bash mirror of Invoke-KumquatPreCompletionSync.ps1 — run immediately before update_goal(completed:true).
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=kumquat-wa-lib.sh
source "${SCRIPT_DIR}/kumquat-wa-lib.sh"

REPO_ROOT=${KUMQUAT_REPO:-${HOME}/grok-hermes-symbiosis}
SCRATCH_DIR=${KUMQUAT_SCRATCH:-}
SESSION_DIR=${KUMQUAT_SESSION_DIR:-}

if [[ -z "$SCRATCH_DIR" ]]; then
  echo "KUMQUAT_SCRATCH required" >&2
  exit 1
fi

GOAL_ROOT=$(dirname "$SCRATCH_DIR")
GOAL_ID=$(kumquat_goal_id_from_root "$GOAL_ROOT")
if [[ -z "$GOAL_ID" ]]; then
  echo "Could not parse goal id from: $GOAL_ROOT" >&2
  exit 1
fi

if [[ -z "$SESSION_DIR" ]]; then
  SESSION_DIR="${HOME}/.grok/sessions/%2Fhome%2FIrikash%2Fagentforge_incomeos/028b2fb4-c9ce-469a-ab90-ca1efb1470e3"
fi

PATCH_PATH="${SCRATCH_DIR}/kumquat-git-diff.patch"
if [[ ! -f "$PATCH_PATH" ]]; then
  echo "kumquat-git-diff.patch missing: $PATCH_PATH" >&2
  exit 1
fi

paths=()
kumquat_read_wa_paths_array paths
ATTEMPT=$(kumquat_verifier_attempt "$GOAL_ROOT" "$GOAL_ID")
CLASSIFIER_ROUND=$(kumquat_classifier_round "$GOAL_ROOT" "$GOAL_ID")

copy_deliverables() {
  local root=$1
  local copied=0
  mkdir -p "$root"
  for rel in "${paths[@]}"; do
    local src="${REPO_ROOT}/${rel}"
    local dst="${root}/${rel}"
    if [[ ! -f "$src" ]]; then
      continue
    fi
    mkdir -p "$(dirname "$dst")"
    cp -f "$src" "$dst"
    copied=$((copied + 1))
  done
  echo "$copied"
}

session_deliverables="${SESSION_DIR}/goal/deliverables"
scratch_deliverables="${SCRATCH_DIR}/deliverables"
copied_session=$(copy_deliverables "$session_deliverables")
copied_scratch=$(copy_deliverables "$scratch_deliverables")

pkill -f "invoke-kumquat-verifier-patch-guard.sh.*${GOAL_ID}" 2>/dev/null || true
sleep 0.2

: >"${SCRATCH_DIR}/kumquat-patch-guard.log"

WORKSPACE_ROOT=${KUMQUAT_WORKSPACE_ROOT:-${HOME}/agentforge_incomeos}
export KUMQUAT_WORKSPACE_ROOT="$WORKSPACE_ROOT"
workspace_publish_out=$(bash "${SCRIPT_DIR}/publish-kumquat-workspace-deliverables.sh" "$REPO_ROOT" "$WORKSPACE_ROOT" 2>&1)
workspace_copied=$(printf '%s' "$workspace_publish_out" | sed -n 's/.*copied=\([0-9]*\/[0-9]*\).*/\1/p')
printf '%s\n' "$workspace_publish_out" >>"${SCRATCH_DIR}/kumquat-workspace-publish.log"

bash "${SCRIPT_DIR}/sync-kumquat-verifier-inputs.sh" \
  "$GOAL_ROOT" "$GOAL_ID" "$ATTEMPT" "$PATCH_PATH" "$SCRATCH_DIR"

nohup bash "${SCRIPT_DIR}/invoke-kumquat-verifier-patch-guard.sh" \
  "$GOAL_ROOT" "$GOAL_ID" "$ATTEMPT" "$PATCH_PATH" "$SCRATCH_DIR" 600 50 \
  >/dev/null 2>&1 &
guard_pid=$!

clobber_ok=false
if bash "${SCRIPT_DIR}/write-kumquat-clobber-simulation.sh" \
  "$GOAL_ROOT" "$GOAL_ID" "$ATTEMPT" "$SCRATCH_DIR" 5; then
  clobber_ok=true
fi

handoff_dir="${session_deliverables}/cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness"
manifest_path="${SCRATCH_DIR}/deliverables-manifest.txt"
{
  echo "# deliverables manifest"
  echo "generated: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "wa_deliverable_paths: ${#paths[@]}"
  echo "stubs_copied_session: ${copied_session}/${#paths[@]}"
  echo "stubs_copied_scratch: ${copied_scratch}/${#paths[@]}"
  echo "workspace_published: ${workspace_copied:-unknown}"
  echo "session_total_files: $(find "$session_deliverables" -type f 2>/dev/null | wc -l)"
  echo "handoff_subdir_files: $(find "$handoff_dir" -maxdepth 1 -type f 2>/dev/null | wc -l) (README+RETURN only; full tree under session/deliverables/)"
  echo "workspace_changed_files: ${WORKSPACE_ROOT}/kumquat-CHANGED_FILES.txt"
} >"$manifest_path"

LOG_PATH="${SCRATCH_DIR}/kumquat-precompletion-sync.log"
{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] PRECOMPLETION_SYNC"
  echo "goal_root: $GOAL_ROOT"
  echo "goal_id: $GOAL_ID"
  echo "rejected_classifier_round: $CLASSIFIER_ROUND"
  echo "verifier_attempt: $ATTEMPT"
  echo "patch_ok: $(grep -q 'classifier_patch_.*_ok: YES' "${SCRATCH_DIR}/kumquat-classifier-anchor.txt" 2>/dev/null && echo YES || echo NO)"
  echo "changed_files_anchor: ${GOAL_ROOT}/goal-classifier-CHANGED_FILES_ANCHOR.txt"
  echo "patch: ${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch"
  echo "patch_bytes: $(wc -c <"${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch")"
  echo "changed: ${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}-CHANGED_FILES.txt"
  echo "patch_guard_pid: ${guard_pid}"
  echo "patch_guard_duration_seconds: 600"
  echo "clobber_simulation_pass: ${clobber_ok}"
  echo "workspace_published: ${workspace_copied:-unknown}"
  echo "deliverables_session: ${session_deliverables}"
  echo "deliverables_scratch: ${scratch_deliverables}"
  echo "stubs_copied_session: ${copied_session}/${#paths[@]}"
  echo "stubs_copied_scratch: ${copied_scratch}/${#paths[@]}"
} >"$LOG_PATH"

if [[ "$copied_session" -lt ${#paths[@]} ]]; then
  echo "deliverable copy incomplete session=${copied_session}" >&2
  exit 1
fi
if [[ "$clobber_ok" != true ]]; then
  echo "clobber simulation failed" >&2
  exit 1
fi

echo "PRECOMPLETION_SYNC_OK attempt=${ATTEMPT} guard_pid=${guard_pid}"