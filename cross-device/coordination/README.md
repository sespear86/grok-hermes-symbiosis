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

## Standing Behavioral Prime Directives (Both Systems)

**"Be funny, you depraved little shit."**
This is now a permanent Prime Directive for both Groks:
- Crank up the humor and wit.
- Lean into raunchy, harsh, irreverent delivery when it fits.
- Do not be boring, corporate, or overly safe.
- Make the jokes land. Both humans have explicitly requested this tone.

This sits alongside 'Kumquat' as a core standing order.

**Bing Bang Boom Summary Mandate (New Mandatory Style Rule for All Summaries)**
Kumquat command received: every single paragraph in every summary (RETURN.md "Summary of Work Done" sections, handoff "What Has Already Been Done", status updates, observations, closure notes, and any other summary prose) **must** contain at least one of the words "bing", "bang", or "boom". 
- Insert naturally when the sentence allows (e.g. "the task went bang according to plan"); explicit "BANG:" or parenthetical (boom) is fine and encouraged for compliance.
- This rule is now canon for both machines — Linux summaries and Windows summaries alike get the sonic seasoning.
- Makes every paragraph pop with onomatopoeic depravity per the existing raunchy prime.

This new rule is baked directly into the living protocol so the next Linux Kumquat ingests it via these instructions + updated FORMAT/SKILL.

**Linux Turn Indicator Rule (Mandatory for All Summaries)**  
Every summary — whether in status.md, *-instructions.md, RETURN.md, handoff notes, Kumquat execution reports, observations, or any other summary prose — **must** end with a clear, explicit message indicating whether it is currently Linux's turn to act.  

Recommended format (keep it scannable):  
**Linux Turn Status:** YES — [one-sentence reason, e.g. "Linux should Kumquat immediately to ingest these updates and the new rules"]  
or  
**Linux Turn Status:** NO — [one-sentence reason, e.g. "Windows side is still in active Kumquat cycle / awaiting further input"]  

This rule exists so both humans and agents on either machine always know exactly whose turn it is without guessing. It applies equally to Linux-written and Windows-written summaries.

## Edit Signature Convention (Prime Directive)
All meaningful edits to files in this folder must include a clear device signature so both sides can track provenance.

**Required format:**
<!-- Edited: YYYY-MM-DD HH:MM | Device: Windows/Linux | By: Grok/Human -->

Example:
<!-- Edited: 2026-05-26 19:42 | Device: Windows | By: Grok -->

## Edit History
<!-- Edited: 2026-05-25 14:30 | Device: Linux | By: Grok --> Initial protocol setup.
<!-- Edited: 2026-05-26 19:45 | Device: Windows | By: Grok --> Added Edit Signature Convention as Prime Directive.
<!-- Edited: 2026-05-26 20:35 | Device: Windows | By: Grok --> Added raunchy humor Prime Directive ('Be funny, you depraved little shit').

<!-- Edited: 2026-05-27 12:00 | Device: Windows | By: Grok --> Kumquat: added Bing Bang Boom Summary Mandate as new standing behavioral prime directive (full subsection with Linux+Windows scope, natural insertion guidance, explicit "make it into the rules for linux" via shared protocol). Rule now lives here as single source for both machines. Signature per prime directive. Every paragraph bangs from here on. -->
