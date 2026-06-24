#!/usr/bin/env bash
# Bash mirror of Sync-KumquatVerifierInputs (KumquatRitualCore.psm1).
# Usage: sync-kumquat-verifier-inputs.sh GOAL_ROOT GOAL_ID ATTEMPT PATCH_PATH [SCRATCH_DIR]
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=kumquat-wa-lib.sh
source "${SCRIPT_DIR}/kumquat-wa-lib.sh"

if [[ $# -lt 4 ]]; then
  echo "USAGE: $0 GOAL_ROOT GOAL_ID ATTEMPT PATCH_PATH [SCRATCH_DIR]" >&2
  exit 2
fi

GOAL_ROOT=$1
GOAL_ID=$2
ATTEMPT=$3
PATCH_PATH=$4
SCRATCH_DIR=${5:-}

if [[ ! -f "$PATCH_PATH" ]]; then
  echo "PATCH_PATH not found: $PATCH_PATH" >&2
  exit 1
fi

first_line=$(head -1 "$PATCH_PATH")
if [[ "$first_line" != "${KUMQUAT_PATCH_MARKER}"* ]]; then
  echo "PATCH_ANCHOR_FAIL first_line=$first_line" >&2
  exit 1
fi

paths=()
kumquat_read_wa_paths_array paths

patch_out="${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch"
changed_out="${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}-CHANGED_FILES.txt"
changed_text=$(kumquat_format_changed_files_list "${paths[@]}")
changed_text+=$'\n'

chmod u+w "$patch_out" 2>/dev/null || true
chmod u+w "$changed_out" 2>/dev/null || true
cp -f "$PATCH_PATH" "$patch_out"
printf '%s' "$changed_text" >"$changed_out"
chmod a-w "$patch_out" "$changed_out"

patch_ok=NO
if [[ "$(head -1 "$patch_out")" == "${KUMQUAT_PATCH_MARKER}"* ]]; then
  patch_ok=YES
fi

if [[ -n "$SCRATCH_DIR" ]]; then
  printf '%s' "$changed_text" >"${SCRATCH_DIR}/CHANGED_FILES.txt"
  printf '%s\n' "${paths[@]}" >"${SCRATCH_DIR}/CHANGED_FILES_ANCHOR.txt"
fi

echo "SYNC_OK attempt=${ATTEMPT} patch=${patch_out} bytes=$(wc -c <"$patch_out") patch_ok=${patch_ok}"
[[ "$patch_ok" == YES ]] || exit 1