#!/usr/bin/env bash
# Grok-Hermes Symbiosis: Quick delegation helper from Grok context to Hermes
# Usage:
#   ./delegate-to-hermes.sh "Task description" [extra prompt context]
#   or pipe context: cat plan.md | ./delegate-to-hermes.sh "Implement this plan"

set -euo pipefail

TASK="${1:-}"
EXTRA="${2:-}"
CONTEXT=""

if [ -z "$TASK" ]; then
  echo "Usage: $0 <task-description> [extra-context]"
  echo "   or: cat context.txt | $0 <task-description>"
  exit 1
fi

# Capture piped stdin as additional context if present
if [ ! -t 0 ]; then
  CONTEXT="$(cat)"
fi

CWD="$(pwd)"
GIT_BRANCH="$(git branch --show-current 2>/dev/null || echo 'no-git')"
GIT_STATUS="$(git status --short 2>/dev/null | head -10 || echo 'no-git-or-clean')"

PROMPT="SYMBIOSIS DELEGATION from Grok Build (grok-4.3 specialist) to Hermes Agent.

Working directory: $CWD
Git branch: $GIT_BRANCH
Recent git status (truncated):
$GIT_STATUS

Task / Goal:
$TASK

Additional context / plan / requirements:
$EXTRA
$CONTEXT

Instructions for Hermes:
- Execute using your full strengths (long-horizon loop, skills, tools, memory, kanban if appropriate).
- If you need deep architecture, multi-reviewer implementation, professional docs (pptx/xlsx/docx), verification, or best-of-n exploration, escalate back using your 'grok-build' skill.
- Prefer clean handoff: produce working results + clear next steps or gateway delivery.
- Use --accept-hooks or yolo behavior only if explicitly safe in the task.

Please begin and report session ID or key outcomes."

# B5 / DESIGN § delegate: optional auto memory push before handoff (best-effort, non-fatal)
# Set SYMBIOSIS_MEMORY_AUTO_PUSH=1 (or device) to enable; uses symbiosis-memory-sync if present.
if [ "${SYMBIOSIS_MEMORY_AUTO_PUSH:-0}" != "0" ]; then
  DEV="${SYMBIOSIS_MEMORY_DEVICE:-Washington Linux}"
  PROJ="${SYMBIOSIS_MEMORY_PROJECT:-grok-hermes-symbiosis}"
  if command -v symbiosis-memory-sync >/dev/null 2>&1; then
    symbiosis-memory-sync push --agent grok --device "$DEV" --project "$PROJ" --dry-run >/dev/null 2>&1 || true
    symbiosis-memory-sync push --agent grok --device "$DEV" --project "$PROJ" 2>/dev/null || echo "[memory-sync] push best-effort (may be dry or palace unavailable)"
  elif [ -x "$(dirname "$0")/../cross-device/scripts/symbiosis-memory-sync" ]; then
    "$(dirname "$0")/../cross-device/scripts/symbiosis-memory-sync" push --agent grok --device "$DEV" --project "$PROJ" 2>/dev/null || true
  fi
fi

echo ">>> Launching Hermes with symbiosis context..."
echo ">>> Task: $TASK"
echo

# Prefer TUI for interactive delegation, but support oneshot for scripting
if [ "${HERMES_ONESHOT:-0}" = "1" ]; then
  exec hermes -z "$PROMPT" --skills grok-build,github,devops
else
  # Interactive TUI with preloaded symbiosis + useful skills
  exec hermes --skills grok-build,github,devops -z "$PROMPT" || exec hermes --skills grok-build

# <!-- Edited: 2026-06-06 | Device: Washington Linux | By: Grok (AUTON c7d73093 reviewer-fix H6 B5) --> Added optional SYMBIOSIS_MEMORY_AUTO_PUSH block (per DESIGN delegate spec) before exec. Non-fatal best-effort. Bing: paste tax reduced. Bang: pre-handoff brain share. Boom: H6 closed. Sig per prime.

fi
