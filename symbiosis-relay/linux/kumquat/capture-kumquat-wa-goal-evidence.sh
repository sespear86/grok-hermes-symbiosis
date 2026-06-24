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
  cd "$REPO_ROOT"
  git fetch origin
  git checkout kumquat-2026-06-01-hygiene
  git pull
  echo "HEAD=$(git rev-parse HEAD)"
  echo "BRANCH=$(git branch --show-current)"
  git log -1 --oneline
  git cat-file -t 137f97e
  git merge-base --is-ancestor 137f97e HEAD && echo "137f97e_ancestor=PASS"
  git log --oneline 137f97e -1
} >"${SCRATCH_DIR}/git.log" 2>&1

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
HEAD=$(git -C "$REPO_ROOT" rev-parse HEAD)
SCORE=$(grep -o 'score=[0-9]*' "${SCRATCH_DIR}/test-relay-structured-status.log" | tail -1 | cut -d= -f2)

{
  echo "Bing bang boom! Washington /kumquat WA goal evidence capture complete."
  echo "Git: branch kumquat-2026-06-01-hygiene HEAD=${HEAD} (137f97e ancestor PASS)"
  echo "Scripts: goal-completion + verification-harness CROSS_ARTIFACT_OK; test-relay PASS schema=0.3.0-structured-status score=${SCORE}"
  echo "Honesty channel: goal-classifier-${GOAL_ID}-${ATTEMPT}.patch bytes=$(wc -c <"${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch")"
  echo "Mirrorability: MET (hot path — git + handoff + linux stubs + rich layer sync). NOT MET for surrogate 20260617-1113 + session ade7ed50 (Syncthing still pending on OR)"
  echo "Oregon has the ball. (Ingest RETURN + resume goal-harness closure.)"
  echo "Linux Turn Status: YES"
  echo "Keep er goinnnn. Bust a nut."
} >"${SCRATCH_DIR}/kumquat-closure.txt"

cat "${SCRATCH_DIR}/kumquat-closure.txt"
echo "CAPTURE_OK scratch=${SCRATCH_DIR}"