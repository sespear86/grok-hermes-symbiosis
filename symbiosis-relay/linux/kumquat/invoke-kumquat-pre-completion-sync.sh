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

bash "${SCRIPT_DIR}/sync-kumquat-verifier-inputs.sh" \
  "$GOAL_ROOT" "$GOAL_ID" "$ATTEMPT" "$PATCH_PATH" "$SCRATCH_DIR"

nohup bash "${SCRIPT_DIR}/invoke-kumquat-verifier-patch-guard.sh" \
  "$GOAL_ROOT" "$GOAL_ID" "$ATTEMPT" "$PATCH_PATH" "$SCRATCH_DIR" 600 50 \
  >/dev/null 2>&1 &
guard_pid=$!

LOG_PATH="${SCRATCH_DIR}/kumquat-precompletion-sync.log"
{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] PRECOMPLETION_SYNC"
  echo "goal_root: $GOAL_ROOT"
  echo "goal_id: $GOAL_ID"
  echo "classifier_round: $CLASSIFIER_ROUND (verifier uses attempt=$((CLASSIFIER_ROUND + 1)))"
  echo "verifier_attempt: $ATTEMPT"
  echo "changed_files_anchor: ${GOAL_ROOT}/goal-classifier-CHANGED_FILES_ANCHOR.txt"
  echo "patch: ${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch"
  echo "patch_bytes: $(wc -c <"${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch")"
  echo "changed: ${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}-CHANGED_FILES.txt"
  echo "patch_guard_pid: ${guard_pid}"
  echo "patch_guard_duration_seconds: 600"
  echo "deliverables_session: ${session_deliverables}"
  echo "deliverables_scratch: ${scratch_deliverables}"
  echo "stubs_copied_session: ${copied_session}/${#paths[@]}"
  echo "stubs_copied_scratch: ${copied_scratch}/${#paths[@]}"
} >"$LOG_PATH"

if [[ "$copied_session" -lt ${#paths[@]} ]]; then
  echo "deliverable copy incomplete session=${copied_session}" >&2
  exit 1
fi

echo "PRECOMPLETION_SYNC_OK attempt=${ATTEMPT} guard_pid=${guard_pid}"