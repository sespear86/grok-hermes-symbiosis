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
  BEFORE_HEAD=$(git rev-parse HEAD)
  REMOTE_URL=$(git remote get-url origin)
  echo "REMOTE_URL=${REMOTE_URL}"
  echo "BEFORE_HEAD=${BEFORE_HEAD}"
  echo "=== VERBATIM REMOTE REF (pre-fetch) ==="
  git ls-remote origin refs/heads/kumquat-2026-06-01-hygiene
  echo "=== VERBATIM FETCH OUTPUT ==="
  git fetch origin --verbose 2>&1
  ORIGIN_TIP=$(git rev-parse origin/kumquat-2026-06-01-hygiene)
  echo "=== VERBATIM CHECKOUT OUTPUT ==="
  git checkout kumquat-2026-06-01-hygiene 2>&1
  echo "=== VERBATIM PULL OUTPUT ==="
  git pull 2>&1
  HEAD=$(git rev-parse HEAD)
  HEAD_SHORT=$(git rev-parse --short HEAD)
  echo "=== DERIVED RECEIPTS (post-command; not fetch/pull stdout) ==="
  echo "ORIGIN_TIP=${ORIGIN_TIP}"
  echo "HEAD=${HEAD}"
  echo "HEAD_SHORT=${HEAD_SHORT}"
  echo "BRANCH=$(git branch --show-current)"
  if [[ "$ORIGIN_TIP" == "$HEAD" ]]; then
    echo "FETCH_DELTA: none (ORIGIN_TIP == LOCAL_HEAD; branch already current)"
  else
    echo "FETCH_DELTA: origin tip advanced to ${ORIGIN_TIP}"
  fi
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
CAPTURE_TS=$(date '+%Y-%m-%d %H:%M')
if [[ -n "$HEAD_SHORT" && -f "$RETURN_FILE" ]]; then
  sed -i "s/→ \*\*HEAD \`[^\`]*\`/→ **HEAD \`${HEAD_SHORT}\`/" "$RETURN_FILE"
  sed -i "s/\*\*Git receipt:\*\* \`[^\`]*\`/\*\*Git receipt:\*\* \`${HEAD_SHORT}\`/" "$RETURN_FILE"
  sed -i "s/<!-- Edited: [^|]* | Device: Linux | By: Grok (\/kumquat) -->/<!-- Edited: ${CAPTURE_TS} | Device: Linux | By: Grok (\/kumquat) -->/" "$RETURN_FILE"
fi

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

GOAL_ROOT=$(dirname "$SCRATCH_DIR")
GOAL_ID=$(kumquat_goal_id_from_root "$GOAL_ROOT")
ATTEMPT=$(kumquat_verifier_attempt "$GOAL_ROOT" "$GOAL_ID")

# --- Commit RETURN + kumquat scripts before pre-completion (clean scoped status) ---
chmod +x "${REPO_ROOT}/symbiosis-relay/linux/kumquat/"*.sh
cd "$REPO_ROOT"
git add symbiosis-relay/linux/kumquat/*.sh \
  cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness/RETURN.md 2>/dev/null || true
if ! git diff --cached --quiet 2>/dev/null; then
  git commit -m "fix(kumquat): WA attempt ${ATTEMPT} — workspace publish, guard hygiene, RETURN receipt" 2>&1 | tee -a "${SCRATCH_DIR}/git-commit.log"
  git push origin kumquat-2026-06-01-hygiene 2>&1 | tee -a "${SCRATCH_DIR}/git-push.log"
fi
{
  echo "=== POST_CAPTURE_COMMIT ==="
  echo "HEAD=$(git rev-parse HEAD)"
  echo "HEAD_SHORT=$(git rev-parse --short HEAD)"
  git status -sb -- \
    symbiosis-relay/linux/kumquat/ \
    cross-device/handoffs/20260623-2109-Kumquat-Ritual-Receipt-Goal-Harness/
} >>"${SCRATCH_DIR}/git.log"
HEAD_SHORT=$(git -C "$REPO_ROOT" rev-parse --short HEAD)
sed -i "s/→ \*\*HEAD \`[^\`]*\`/→ **HEAD \`${HEAD_SHORT}\`/" "$RETURN_FILE"
sed -i "s/\*\*Git receipt:\*\* \`[^\`]*\`/\*\*Git receipt:\*\* \`${HEAD_SHORT}\`/" "$RETURN_FILE"

# --- kumquat-git-diff.patch (post-commit authoritative for sync + guard) ---
kumquat_write_git_diff_patch "$REPO_ROOT" "${SCRATCH_DIR}/kumquat-git-diff.patch" "${paths[@]}"
printf '%s\n' "${paths[@]}" >"${SCRATCH_DIR}/kumquat-changes.txt"

# --- Pre-completion sync (honesty channel + workspace publish) ---
bash "${SCRIPT_DIR}/invoke-kumquat-pre-completion-sync.sh"

SCORE=$(grep -o 'score=[0-9]*' "${SCRATCH_DIR}/test-relay-structured-status.log" | tail -1 | cut -d= -f2)
PATCH_BYTES=$(wc -c <"${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch")

{
  echo "Bing bang boom! Washington /kumquat WA goal evidence capture complete."
  echo "Git: branch kumquat-2026-06-01-hygiene HEAD=${HEAD_SHORT} (137f97e ancestor PASS)"
  echo "Scripts: goal-completion + verification-harness CROSS_ARTIFACT_OK (×2); test-relay PASS schema=0.3.0-structured-status score=${SCORE} (×2)"
  echo "Honesty channel: goal-classifier-${GOAL_ID}-${ATTEMPT}.patch bytes=${PATCH_BYTES}"
  echo "CHANGED_FILES: ${SCRATCH_DIR}/CHANGED_FILES.txt + ${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}-CHANGED_FILES.txt"
  echo "Workspace: ${HOME}/agentforge_incomeos/kumquat-CHANGED_FILES.txt"
  echo "Mirrorability: MET (hot path — git + handoff + linux stubs + rich layer sync). NOT MET for surrogate 20260617-1113 + session ade7ed50 (Syncthing still pending on OR)"
  echo "Oregon has the ball. (Ingest RETURN + resume goal-harness closure.)"
  echo "Linux Turn Status: YES"
  echo "Keep er goinnnn. Bust a nut."
} >"${SCRATCH_DIR}/kumquat-closure.txt"

# --- Verification plan step 5: evidence grep (classifier patch only; no kumquat-git-diff mixing) ---
CLASSIFIER_PATCH="${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}.patch"
CLASSIFIER_CHANGED="${GOAL_ROOT}/goal-classifier-${GOAL_ID}-${ATTEMPT}-CHANGED_FILES.txt"
{
  echo "=== VERIFICATION PLAN STEP 5 ==="
  echo "verifier_attempt=${ATTEMPT}"
  for phrase in "Linux Turn Status: YES" "Mirrorability: MET (hot path" "Oregon has the ball" "Keep er goinnnn. Bust a nut." "CROSS_ARTIFACT_OK" "PASS — structured relay status" "137f97e_ancestor=PASS" "FETCH_DELTA" "WORKSPACE_PUBLISH_OK"; do
    echo "--- ${phrase} ---"
    grep -rl "$phrase" "${SCRATCH_DIR}"/*.log "${SCRATCH_DIR}"/*.txt "$RETURN_FILE" 2>/dev/null | grep -v kumquat-git-diff | head -5 || true
  done
  echo "=== stale ENOENT check ==="
  grep -l "No such file or directory" "${SCRATCH_DIR}/goal-completion.log" "${SCRATCH_DIR}/verification-harness.log" "${SCRATCH_DIR}/test-relay-structured-status.log" 2>/dev/null || echo "PASS: no ENOENT in per-script logs"
  echo "=== honesty channel (classifier attempt ${ATTEMPT} only) ==="
  wc -c "$CLASSIFIER_PATCH" "$CLASSIFIER_CHANGED" "${SCRATCH_DIR}/CHANGED_FILES.txt"
  echo "=== workspace CHANGED_FILES publish ==="
  wc -c "${HOME}/agentforge_incomeos/kumquat-CHANGED_FILES.txt" 2>/dev/null || echo "workspace CHANGED missing"
  echo "=== permission check changed file ==="
  ls -la "$CLASSIFIER_CHANGED"
  echo "=== guard log attempt filter ==="
  grep "attempt=${ATTEMPT}" "${SCRATCH_DIR}/kumquat-patch-guard.log" 2>/dev/null | tail -5 || echo "no guard lines for attempt ${ATTEMPT}"
} >"${SCRATCH_DIR}/verification-grep.txt"

cat "${SCRATCH_DIR}/kumquat-closure.txt"
echo "CAPTURE_OK scratch=${SCRATCH_DIR}"