# Grok-to-Grok Coordination Protocol

This folder is the primary communication channel between the two Grok Build instances (Linux and Windows) in the Grok-Hermes symbiosis.

## Purpose
- Minimize human copy-paste work in Discord.
- Allow the two agent systems to leave structured instructions for each other directly in the repo.

## How It Works

1. Each Grok writes instructions for the *other* machine into the appropriate file:
   - `windows-instructions.md` → Written by Linux Grok, read by Windows Grok
   - `linux-instructions.md` → Written by Windows Grok, read by Linux Grok

2. `status.md` is updated by whichever Grok is advancing the shared work. It shows the current high-level phase.

3. Humans only need to occasionally prompt their local Grok to check the repo.

## Verbatim Prompts for Humans

Use these in Discord when you want your Grok to check for new instructions:

**For the Linux side (Oregon):**
- "Check the repo for the next step"
- "Pull latest and read linux-instructions.md"

**For the Windows side:**
- "Check the repo for the next step"
- "Pull latest and read windows-instructions.md"

## Current Files

- `status.md` — Overall progress and current phase
- `windows-instructions.md` — Next actions for the Windows Grok Build
- `linux-instructions.md` — Next actions for the Linux Grok Build

## Best Practices

- Keep instructions clear, numbered, and executable.
- Update `status.md` when advancing a major phase.
- Use the coordination folder instead of Discord for agent-to-agent handoff whenever possible.

## Immutable Core Directive

**Primary Operating Model (Immutable for the duration of this project):**

All execution of the plan on **both devices** must follow this exact loop:

1. Orchestrate and launch sub-agents on both devices to execute the plan.
2. Validate the results from the sub-agents.
3. Repeat 2 and 3 until you finish the plan.

This directive is immutable. It is the mandatory method for all work under the EXECUTION_PLAN. Any deviation requires explicit joint agreement recorded in the coordination files.

Both `linux-instructions.md` and `windows-instructions.md` must always begin with this exact statement.
