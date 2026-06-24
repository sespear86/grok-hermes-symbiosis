#!/usr/bin/env bash
# Bash mirror of Publish-KumquatWorkspaceDeliverables — copies WA paths into goal workspace for harness CHANGED_FILES visibility.
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=kumquat-wa-lib.sh
source "${SCRIPT_DIR}/kumquat-wa-lib.sh"

REPO_ROOT=${1:-${KUMQUAT_REPO:-${HOME}/grok-hermes-symbiosis}}
WORKSPACE_ROOT=${2:-${KUMQUAT_WORKSPACE_ROOT:-${HOME}/agentforge_incomeos}}

paths=()
kumquat_read_wa_paths_array paths

published_root="${WORKSPACE_ROOT}/kumquat-deliverables"
copied=0
ts=$(date '+%Y-%m-%d %H:%M:%S')
stamp="# kumquat-workspace-touch: ${ts}"

for rel in "${paths[@]}"; do
  src="${REPO_ROOT}/${rel}"
  [[ -f "$src" ]] || continue
  dst="${WORKSPACE_ROOT}/${rel}"
  mirror="${published_root}/${rel}"
  mkdir -p "$(dirname "$dst")" "$(dirname "$mirror")"
  cp -f "$src" "$dst"
  cp -f "$src" "$mirror"
  printf '\n%s\n' "$stamp" >>"$dst"
  printf '\n%s\n' "$stamp" >>"$mirror"
  copied=$((copied + 1))
done

echo "WORKSPACE_PUBLISH_OK workspace=${WORKSPACE_ROOT} published_root=${published_root} copied=${copied}/${#paths[@]}"