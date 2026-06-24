#!/usr/bin/env bash
# Shared helpers for Washington /kumquat goal-harness honesty channel (bash mirror of KumquatRitualCore).
set -euo pipefail

KUMQUAT_PATCH_MARKER="# Kumquat git diff anchor"

kumquat_wa_deliverable_paths() {
  cat <<'PATHS'
symbiosis-relay/linux/kumquat/kumquat-wa-lib.sh
symbiosis-relay/linux/kumquat/sync-kumquat-verifier-inputs.sh
symbiosis-relay/linux/kumquat/invoke-kumquat-pre-completion-sync.sh
symbiosis-relay/linux/kumquat/invoke-kumquat-verifier-patch-guard.sh
symbiosis-relay/linux/kumquat/capture-kumquat-wa-goal-evidence.sh
cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness/RETURN.md
cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness/README.md
cross-device/coordination/status.md
cross-device/coordination/linux-instructions.md
cross-device/handoffs/HANDOFF_LOG.md
Mempalace/symbiosis/device-presence/oregon.md
Mempalace/symbiosis/device-presence/washington.md
PATHS
}

kumquat_goal_id_from_root() {
  local goal_root=$1
  basename "$goal_root" | sed -n 's/^grok-goal-\([a-z0-9]*\)$/\1/p'
}

kumquat_classifier_round() {
  local goal_root=$1 goal_id=$2
  local latest_verdict round
  latest_verdict=$(ls -t "$goal_root"/goal-verdict-"${goal_id}"-*.json 2>/dev/null | head -1 || true)
  if [[ -n "$latest_verdict" ]]; then
    round=$(basename "$latest_verdict" | sed -n "s/^goal-verdict-${goal_id}-\([0-9][0-9]*\)-.*/\1/p")
    if [[ -n "$round" ]]; then
      echo "$round"
      return 0
    fi
  fi
  local latest_md
  latest_md=$(ls -t "$goal_root"/goal-classifier-"${goal_id}"-*.md 2>/dev/null | grep -v skeptic | head -1 || true)
  if [[ -n "$latest_md" ]]; then
    round=$(basename "$latest_md" | sed -n "s/^goal-classifier-${goal_id}-\([0-9][0-9]*\)\.md$/\1/p")
    if [[ -n "$round" ]]; then
      echo "$round"
      return 0
    fi
  fi
  echo 0
}

kumquat_verifier_attempt() {
  local goal_root=$1 goal_id=$2
  if [[ -n "${KUMQUAT_VERIFIER_ATTEMPT:-}" ]]; then
    echo "$KUMQUAT_VERIFIER_ATTEMPT"
    return 0
  fi
  local round
  round=$(kumquat_classifier_round "$goal_root" "$goal_id")
  if [[ "$round" -gt 0 ]]; then
    echo $((round + 1))
  else
    echo 1
  fi
}

kumquat_read_wa_paths_array() {
  local -n _out=$1
  _out=()
  while IFS= read -r line; do
    [[ -n "$line" ]] && _out+=("$line")
  done < <(kumquat_wa_deliverable_paths)
}

kumquat_format_changed_files_list() {
  local paths=("$@")
  echo "# CHANGED_FILES (verifier sync - canonical grok-hermes-symbiosis paths)"
  echo "# path_count: ${#paths[@]}"
  echo
  printf '%s\n' "${paths[@]}"
}

kumquat_patch_needs_repair() {
  local patch_path=$1
  if [[ ! -f "$patch_path" ]]; then
    return 0
  fi
  local first
  first=$(head -1 "$patch_path" 2>/dev/null || true)
  [[ "$first" != "${KUMQUAT_PATCH_MARKER}"* ]]
}

kumquat_write_git_diff_patch() {
  local repo_root=$1 patch_path=$2
  shift 2
  local paths=("$@")
  local head ts
  head=$(git -C "$repo_root" rev-parse HEAD)
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  {
    echo "${KUMQUAT_PATCH_MARKER} (repo-scoped; goal-classifier CHANGED_FILES cannot see grok-hermes-symbiosis)"
    echo "# Generated: ${ts} run=wa-capture repo=${repo_root}"
    echo "# HEAD: ${head}"
    echo "# Canonical paths: ${#paths[@]} (see CHANGED_FILES_ANCHOR.txt + deliverables/)"
    echo
    echo "## SECTION A: working tree diff vs HEAD (WA deliverable paths)"
    echo
    git -C "$repo_root" diff HEAD -- "${paths[@]}"
    echo
    echo "## SECTION B: 137f97e..HEAD (WA ingest range)"
    echo
    git -C "$repo_root" diff 137f97e..HEAD -- "${paths[@]}" 2>/dev/null || true
  } >"$patch_path"
}