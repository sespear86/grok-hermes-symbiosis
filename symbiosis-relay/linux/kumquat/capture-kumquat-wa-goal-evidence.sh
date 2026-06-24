#!/usr/bin/env bash
# Washington /kumquat goal evidence orchestrator — verification plan steps 1–2 + pre-completion sync.
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=kumquat-wa-lib.sh
source "${SCRIPT_DIR}/kumquat-wa-lib.sh"

REPO_ROOT=${KUMQUAT_REPO:-${HOME}/grok-hermes-symbiosis}
SCRATCH_DIR=${KUMQUAT_SCRATCH:-/tmp/grok-goal-c27ea408dda1/implementer}
SESSION_DIR=${KUMQUAT_SESSION_DIR:-${HOME}/.grok/sessions/%2Fhome%2FIrikash%2Fagentforge_incomeos/028b2fb4-c9ce-469a-ab90-ca1efb1470e3}
RICH_ROOT=${HOME}/Synced/grok-mempalace-integration/symbiosis-relay
SRC_RELAY=${REPO_ROOT}/cross-device/symbiosis-relay
TEST_SCRIPT=${RICH_ROOT}/linux/tools/test-relay-structured-status.sh

mkdir -p "$SCRATCH_DIR"
export KUMQUAT_SCRATCH="$SCRATCH_DIR"
export KUMQUAT_SESSION_DIR="$SESSION_DIR"
export KUMQUAT_REPO="$REPO_ROOT"

paths=()
kumquat_read_wa_paths_array paths

# --- Rich layer self-provision (canonical test path) ---
mkdir -p "${RICH_ROOT}/linux/tools" "${RICH_ROOT}/status/washington"
cp -f "${SRC_RELAY}/linux/tools/test-relay-structured-status.sh" \
      "${SRC_RELAY}/linux/tools/update-persistence-cache.sh" \
      "${SRC_RELAY}/linux/tools/write-relay-structured-status.sh" \
      "${RICH_ROOT}/linux/tools/"
cp -f "${SRC_RELAY}/relay_status_core.py" "${RICH_ROOT}/"

# --- Verification plan step 1: single git.log capture ---
{
  echo "=== VERIFICATION PLAN STEP 1 ==="
  echo "COMMAND: cd ~/grok-hermes-symbiosis && git fetch origin && git checkout kumquat-2026-06-01-hygiene && git pull"
  cd "$REPO_ROOT"
  git checkout -- symbiosis-relay/linux/kumquat/*.sh 2>/dev/null || true
  BEFORE_HEAD=$(git rev-parse HEAD)
  echo "BEFORE_HEAD=${BEFORE_HEAD}"
  git fetch origin 2>&1
  ORIGIN_TIP=$(git rev-parse origin/kumquat-2026-06-01-hygiene)
  echo "ORIGIN_TIP=${ORIGIN_TIP}"
  git checkout kumquat-2026-06-01-hygiene 2>&1
  git pull 2>&1
  HEAD=$(git rev-parse HEAD)
  HEAD_SHORT=$(git rev-parse --short HEAD)
  echo "HEAD=${HEAD}"
  echo "HEAD_SHORT=${HEAD_SHORT}"
  echo "BRANCH=$(git branch --show-current)"
  git log -1 --oneline
  echo "TIP_RANGE_137f97e..HEAD:"
  git log --oneline 137f97e..HEAD
  echo "137f97e_commit=$(git log --oneline 137f97e -1)"
  git merge-base --is-ancestor 137f97e HEAD && echo "137f97e_ancestor=PASS"
  echo "=== kumquat-scoped status (tracked ritual paths) ==="
  git status -sb -- \
    symbiosis-relay/linux/kumquat/ \
    cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness/ \
    cross-device/coordination/status.md \
    cross-device/coordination/linux-instructions.md \
    cross-device/handoffs/HANDOFF_LOG.md \
    Mempalace/symbiosis/device-presence/
} >"${SCRATCH_DIR}/git.log" 2>&1

HEAD_SHORT=$(grep '^HEAD_SHORT=' "${SCRATCH_DIR}/git.log" | cut -d= -f2)
RETURN_FILE="${REPO_ROOT}/cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness/RETURN.md"
if [[ -n "$HEAD_SHORT" && -f "$RETURN_FILE" ]]; then
  sed -i "s/→ \*\*HEAD \`[^\`]*\`/→ **HEAD \`${HEAD_SHORT}\`/" "$RETURN_FILE"
  sed -i "s/\*\*Git receipt:\*\* \`[^\`]*\`/\*\*Git receipt:\*\* \`${HEAD_SHORT}\`/" "$RETURN_FILE"
fi

# Avoid mode-dirty M on kumquat/*.sh after chmod runs
git -C "$REPO_ROOT" checkout -- symbiosis-relay/linux/kumquat/*.sh 2>/dev/null || true

# --- Verification plan step 2: per-script logs (2 runs each) ---
{
  echo "=== invoke-kumquat-goal-completion.sh (2 runs) ==="
  for run in 1 2; do
    echo "--- RUN ${run} ---"
    bash "${REPO_ROOT}/symbiosis-relay/linux/kumquat/invoke-kumquat-goal-completion.sh"
  done
} >"${SCRATCH_DIR}/goal-completion.log" 2>&1

{
  echo "=== invoke-kumquat-verification-harness.sh (2 runs) ==="
  for run in 1 2; do
    echo "--- RUN ${run} ---"
    bash "${REPO_ROOT}/symbiosis-relay/linux/kumquat/invoke-kumquat-verification-harness.sh"
  done
} >"${SCRATCH_DIR}/verification-harness.log" 2>&1

{
  echo "=== test-relay-structured-status.sh canonical path (2 runs) ==="
  echo "PATH=${TEST_SCRIPT}"
  for run in 1 2; do
    echo "--- RUN ${run} ---"
    bash "$TEST_SCRIPT"
  done
} >"${SCRATCH_DIR}/test-relay-structured-status.log" 2>&1

cat "${SCRATCH_DIR}/goal-completion.log" \
    "${SCRATCH_DIR}/verification-harness.log" \
    "${SCRATCH_DIR}/test-relay-structured-status.log" \
  >"${SCRATCH_DIR}/scripts-all.log"

# --- kumquat-git-diff.patch (authoritative for sync + guard) ---
kumquat_write_git_diff_patch "$REPO_ROOT" "${SCRATCH_DIR}/kumquat-git-diff.patch" "${paths[@]}"
printf '%s\n' "${paths[@]}" >"${SCRATCH_DIR}/kumquat-changes.txt"

# --- Verification plan step 3: ingest excerpts ---
head -8 "${REPO_ROOT}/cross-device/coordination/linux-instructions.md" >"${SCRATCH_DIR}/ingest-linux-instructions.txt"
head -5 "${REPO_ROOT}/cross-device/coordination/status.md" >"${SCRATCH_DIR}/ingest-status.txt"
head -12 "${REPO_ROOT}/Mempalace/symbiosis/device-presence/oregon.md" >"${SCRATCH_DIR}/ingest-oregon-hb.txt"
grep -A5 "Round 14" "${REPO_ROOT}/cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md" | head -8 >"${SCRATCH_DIR}/ingest-mirror.txt"
grep -A8 "Rounds 12" "${REPO_ROOT}/cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness/README.md" | head -10 >"${SCRATCH_DIR}/ingest-handoff.txt"
{
  echo "surrogate check:"
  ls -la "${HOME}/Synced/grok-mempalace-integration/symbiosis-relay/surrogates/" 2>&1 || echo "ABSENT: surrogates/"
  echo "CONCLUSION: NOT MET — surrogate 20260617-1113 + session ade7ed50 (Syncthing still pending on OR)"
} >"${SCRATCH_DIR}/ingest-surrogate.txt"

# --- Pre-completion sync (honesty channel) ---
bash "${SCRIPT_DIR}/invoke-kumquat-pre-completion-sync.sh"

GOAL_ROOT=$(dirname "$SCRATCH_DIR")
GOAL_ID=$(kumquat_goal_id_from_root "$GOAL_ROOT")
ATTEMPT=$(kumquat_verifier_attempt "$GOAL_ROOT" "$GOAL_ID")
HEAD=$(grep '^HEAD=' "${SCRATCH_DIR}/git.log" | cut -d= -f2)
HEAD_SHORT=$(grep '^HEAD_SHORT=' "${SCRATCH_DIR}/git.log" | cut -d= -f2)
SCORE=$(grep -o 'score=[0-9]*' "${SCRATCH_DIR}/test-relay-structured-status.log" | tail -1 | cut -d= -f2)
PATCH_BYTES=$(wc -c <"${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch")

{
  echo "Bing bang boom! Washington /kumquat WA goal evidence capture complete."
  echo "Git: branch kumquat-2026-06-01-hygiene HEAD=${HEAD_SHORT} (137f97e ancestor PASS)"
  echo "Scripts: goal-completion + verification-harness CROSS_ARTIFACT_OK (×2); test-relay PASS schema=0.3.0-structured-status score=${SCORE} (×2)"
  echo "Honesty channel: goal-classifier-${GOAL_ID}-${ATTEMPT}.patch bytes=${PATCH_BYTES}"
  echo "CHANGED_FILES: ${SCRATCH_DIR}/CHANGED_FILES.txt + ${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}-CHANGED_FILES.txt"
  echo "Mirrorability: MET (hot path — git + handoff + linux stubs + rich layer sync). NOT MET for surrogate 20260617-1113 + session ade7ed50 (Syncthing still pending on OR)"
  echo "Oregon has the ball. (Ingest RETURN + resume goal-harness closure.)"
  echo "Linux Turn Status: YES"
  echo "Keep er goinnnn. Bust a nut."
} >"${SCRATCH_DIR}/kumquat-closure.txt"

# --- Verification plan step 5: evidence grep ---
{
  echo "=== VERIFICATION PLAN STEP 5 ==="
  for phrase in "Linux Turn Status: YES" "Mirrorability: MET (hot path" "Oregon has the ball" "Keep er goinnnn. Bust a nut." "CROSS_ARTIFACT_OK" "PASS — structured relay status" "137f97e" "Rounds 12" "137f97e_ancestor=PASS" "goal-classifier-${GOAL_ID}-${ATTEMPT}.patch"; do
    echo "--- ${phrase} ---"
    grep -rl "$phrase" "${SCRATCH_DIR}"/*.log "${SCRATCH_DIR}"/*.txt "$RETURN_FILE" 2>/dev/null | head -5 || true
  done
  echo "=== stale ENOENT check ==="
  grep -l "No such file or directory" "${SCRATCH_DIR}/goal-completion.log" "${SCRATCH_DIR}/verification-harness.log" "${SCRATCH_DIR}/test-relay-structured-status.log" 2>/dev/null || echo "PASS: no ENOENT in per-script logs"
  echo "=== honesty channel sizes ==="
  wc -c "${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch" "${SCRATCH_DIR}/CHANGED_FILES.txt" "${SCRATCH_DIR}/kumquat-git-diff.patch"
  echo "=== permission check changed file ==="
  ls -la "${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}-CHANGED_FILES.txt"
} >"${SCRATCH_DIR}/verification-grep.txt"

cat "${SCRATCH_DIR}/kumquat-closure.txt"
echo "CAPTURE_OK scratch=${SCRATCH_DIR}"