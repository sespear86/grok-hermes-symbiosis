#!/usr/bin/env bash
# Grok-Hermes Symbiosis: Quick delegation helper from Hermes context to Grok Build
# Usage inside Hermes or from shell:
#   ./delegate-to-grok.sh "Task for Grok specialist" [extra]
#   cat spec.md | ./delegate-to-grok.sh "Implement with full review loop"

set -euo pipefail

TASK="${1:-}"
EXTRA="${2:-}"
CONTEXT=""

if [ -z "$TASK" ]; then
  echo "Usage: $0 <task-for-grok> [extra-context]"
  exit 1
fi

if [ ! -t 0 ]; then
  CONTEXT="$(cat)"
fi

CWD="$(pwd)"
GIT_INFO="$(git branch --show-current 2>/dev/null || true; git status --short 2>/dev/null | head -5 || true)"

PROMPT="SYMBIOSIS ESCALATION from Hermes Agent to Grok Build TUI (xAI grok-4.3 SE specialist).

Working directory: $CWD
Git context:
$GIT_INFO

Task for Grok specialist:
$TASK

Additional context / spec / previous work:
$EXTRA
$CONTEXT

Recommended Grok workflows (choose as appropriate):
- implement (with reviewers) for coding/features
- design (full design-doc + reviewer loop) for architecture
- check for independent verification
- best-of-n for exploring multiple approaches
- review for code review
- pptx / xlsx / docx for professional polished output
- plan mode if high ambiguity

After completion, summarize results + file paths. If long-running execution, gateway delivery, or persistence is needed afterward, hand back to Hermes via the 'hermes' skill.

Begin using the most suitable Grok Build capability."
echo ">>> Delegating to Grok Build..."
echo ">>> Task: $TASK"

# Use oneshot for clean integration from Hermes; user can always continue interactively
exec grok -z "$PROMPT" --best-of-n 1 2>/dev/null || exec grok -z "$PROMPT"
