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

**For the Linux side (Washington):**
- "Kumquat"
- "Pull latest from the repo, read and execute linux-instructions.md"

**For the Windows side (Oregon):**
- "Kumquat"
- "Pull latest from the repo, read and execute windows-instructions.md"

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

**Linux Turn Indicator Rule (Mandatory for All Summaries)**  
Every summary — whether in status.md, *-instructions.md, RETURN.md, handoff notes, Kumquat execution reports, observations, or any other summary prose — **must** end with a clear, explicit message indicating whether it is currently Linux's turn to act.  

Recommended format (keep it scannable):  
**Linux Turn Status:** YES — [one-sentence reason, e.g. "Linux should Kumquat immediately to ingest these updates and the new rules"]  
or  
**Linux Turn Status:** NO — [one-sentence reason, e.g. "Windows side is still in active Kumquat cycle / awaiting further input"]  

This rule exists so both humans and agents on either machine always know exactly whose turn it is without guessing. It applies equally to Linux-written and Windows-written summaries.

**Mirrorability / Full Provisioning Prime (New Standing Directive)**:  
Whenever you create, extend, or significantly modify any part of the system (new scripts, services, packages, tools, configs, systemd units/timers, helpers, features, launchers, etc.), you **must** simultaneously deliver everything the other device needs to replicate it quickly, reliably, and with minimal friction.  
This includes (but is not limited to):  
- Exact package names, versions, install/venv/pip commands, or equivalent  
- Complete script contents (or precise repo paths + permissions)  
- Full systemd service/timer files or Windows Task Scheduler / launcher equivalents  
- Configuration snippets, environment variables, PATH / alias requirements  
- Verification, self-test, or health-check commands  
- Any platform-specific adaptation notes (Linux vs Windows paths, PowerShell vs bash differences, one-liner ports)  
- Dependencies on openclaw, tmux helpers, screenshot tools, etc.  

The explicit goal is "no asymmetric creep" and "the other side can stand this up in one focused session from the artifacts alone." Never leave the brother machine guessing or requiring follow-up DMs for basics.

## Edit Signature Convention (Prime Directive)
All meaningful edits to files in this folder must include a clear device signature so both sides can track provenance.

**Required format:**
<!-- Edited: YYYY-MM-DD HH:MM | Device: Windows/Linux | By: Grok/Human -->

Example:
<!-- Edited: 2026-05-26 19:42 | Device: Windows | By: Grok -->

## Mirrorability Prime Enforcement (New)

The master living document that makes the entire symbiosis stack mirrorable is:

**`MIRROR_KITS_AND_INFRASTRUCTURE.md`**

- Primary (live, Syncthing): `~/Synced/grok-mempalace-integration/symbiosis-relay/MIRROR_KITS_AND_INFRASTRUCTURE.md`
- Git reference: `cross-device/MIRROR_KITS_AND_INFRASTRUCTURE.md`

Every component (Mempalace, Relay stack, Bust a Nut recovery, local tooling, hooks, Pi bring-up, etc.) must have complete mirror instructions there before it is considered done. This document was created by retroactively applying the Mirrorability Prime to all prior progress.

## Edit History
<!-- Edited: 2026-05-25 14:30 | Device: Linux | By: Grok --> Initial protocol setup.
<!-- Edited: 2026-05-26 19:45 | Device: Windows | By: Grok --> Added Edit Signature Convention as Prime Directive.
<!-- Edited: 2026-05-26 20:35 | Device: Windows | By: Grok --> Added raunchy humor Prime Directive ('Be funny, you depraved little shit').

<!-- Edited: 2026-05-27 12:00 | Device: Windows | By: Grok --> Kumquat: added Bing Bang Boom Summary Mandate as new standing behavioral prime directive (full subsection with Linux+Windows scope, natural insertion guidance, explicit "make it into the rules for linux" via shared protocol). Rule now lives here as single source for both machines. Signature per prime directive. Every paragraph bangs from here on. -->

<!-- Edited: 2026-05-28 | Device: Linux | By: Grok --> Kumquat explicit ritual canonized system-wide per user directive: "Kumquat now explicitly means 'Pull latest from the repo, read and execute Linux-instructions.md' on Linux and 'Pull latest from the repo, read and execute Windows-instructions.md' on Windows". Updated SKILL.md (prime + header), windows-instructions.md (Kumquat bullet), this README (verbatim prompts to full ritual phrasing + nuked stale bing-bang-boom subsection entirely). Linux Turn and other primes untouched. Raunchy filth preserved, exact sig applied. The nervous system just got its trigger ritual locked in the dirtiest, most unambiguous way. Signature per prime directive. Keep er goinnnn, you ritual-fucking degenerates. -->

<!-- Edited: 2026-05-30 02:27 | Device: Linux | By: Grok (Mirrorability Prime enforcement) --> Added pointer + explanation in coordination/README.md to the new master `MIRROR_KITS_AND_INFRASTRUCTURE.md` (created in rich project + git reference). This is the primary artifact for retroactive + ongoing application of the Mirrorability Prime to the entire existing symbiosis stack. Rich backdated signatures + full mirror recipes live in the document itself. Signature per prime directive. Keep er goinnnn, you nervous-system-enforcing degenerates. -->

<!-- Edited: 2026-05-30 02:37 | Device: Linux | By: Grok (Mirrorability Prime - Windows porting) --> Created easy-install PowerShell script + polished quickstart guide in `symbiosis-relay/windows/` so Oregon can mirror the current full stack with one command after normal Kumquat + Syncthing. Updated master mirror doc and coordination pointers. Direct, high-leverage fulfillment of the prime's "make it easy for the other device" requirement. Signature per prime directive. Keep er goinnnn, you Oregon-enabling degenerates. Bust a nut. -->

<!-- Edited: 2026-05-28 15:30 | Device: Linux | By: Grok (backdated per Mirrorability Prime) --> Introduced the Mirrorability / Full Provisioning Prime as a core standing directive. Full prime text inserted into Standing Behavioral Prime Directives section (right after the Linux Turn Indicator Rule). This change was made to satisfy the explicit user requirement that new system components must always ship with complete mirror kits. 

To mirror this exact change on the other device:
1. In coordination/README.md: Insert the full Mirrorability section after the Linux Turn Indicator Rule paragraph and before "## Edit Signature Convention".
2. In both linux-instructions.md and windows-instructions.md: Insert the prime as a new bullet immediately after the "Bust a nut" section (before any "Bust a Nut trigger received" notes).
3. In both SKILL.md files (repo + ~/.grok/skills/cross-device/): Update the header to include "+ Mirrorability" and add the prime description after the "Don't stop to ask..." / Prime #5 section.
4. Add rich backdated signatures (this format) in all locations.
5. Optional but recommended: Add a short note in Mempalace/symbiosis/recent-decisions.md under a "2026-05-28 Prime Expansion" section.

Full text of the new prime (use exactly this wording):

**Mirrorability / Full Provisioning Prime (New Standing Directive)**:  
Whenever you create, extend, or significantly modify any part of the system (new scripts, services, packages, tools, configs, systemd units/timers, helpers, features, launchers, etc.), you **must** simultaneously deliver everything the other device needs to replicate it quickly, reliably, and with minimal friction. This includes (but is not limited to): exact package names, versions, install/venv/pip commands, complete script contents (or precise repo paths + permissions), full systemd service/timer files or Windows equivalents, configuration snippets, environment variables, PATH/alias requirements, verification/self-test/health-check commands, and any platform-specific adaptation notes (Linux vs Windows paths, PowerShell vs bash, one-liner ports). Dependencies on openclaw, tmux helpers, screenshot tools, etc. must also be called out. The explicit goal is zero "you had to be there" situations — the brother machine must be able to stand the new component up in one focused session using only the artifacts left in the repo, Mempalace, coordination/, or handoff packages. No asymmetric creep allowed. This prime is now on equal footing with Kumquat, raunchy humor, signatures, self-test, autonomous momentum, and Bust a nut.

Signature per prime directive (backdated for historical accuracy during the 2026-05-27/28 prime formalization wave). This edit itself obeys the prime it introduces. Keep er goinnnn, you provenance-fixing, mirror-kit-documenting degenerates. -->
