---
name: grok-build
description: >
  Delegate specialized software engineering, architecture design, rigorous verification, professional document generation (pptx/xlsx/docx), parallel exploration (best-of-n), and high-ambiguity planning to the local Grok Build TUI on this machine.
  This is the reciprocal symbiosis skill to the "hermes" skill. Use when Hermes needs deep SE specialist capabilities from Grok Build.
  Part of the cross-device Grok-Hermes symbiosis.
version: 1.1.0
author: Grok-Hermes Symbiosis
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [Grok, xAI, Symbiosis, SE-Specialist, Design, Review, Verification, BestOfN, ProfessionalDocs, CrossDevice]
    related_skills: [hermes, cross-device]
    requires_toolsets: [terminal]
---

# Grok Build Specialist — Symbiosis Skill (Windows-adapted)

## Behavioral Prime Directives (Symbiosis-Wide)

These rules apply to all summaries, reports, and artifacts produced when using or responding via this skill:

**Bing Bang Boom Rule**  
Every paragraph in every summary must contain at least one of the words "bing", "bang", or "boom".

**Linux Turn Indicator Rule**  
Every summary must end with a clear line in this format:  
**Linux Turn Status:** YES — [reason]  
or  
**Linux Turn Status:** NO — [reason]

Full details and enforcement live in `cross-device/coordination/README.md` and the cross-device skill.

---

This skill allows Hermes to intelligently delegate to the local **Grok Build TUI** (the deep software engineering specialist running on the same machine).

## When to Use

- User or current task requires rigorous multi-step SE work, architecture, or verification.
- Need professional output (slides, specs, spreadsheets).
- Complex coding/refactoring where quality and review matter.
- Parallel exploration of approaches (`best-of-n`).
- Independent code review or verification of work done so far.
- High-ambiguity tasks that benefit from plan mode or design loops.

**Do NOT use** for simple commands, long-running monitoring, or gateway delivery — those are Hermes strengths.

## Delegation Patterns (Windows)

### Preferred: Use the bridge script
```powershell
hermes-grok-delegate "Detailed task description here. Include relevant context, files, and success criteria."
```

Or the full path if needed:
```powershell
& "$env:USERPROFILE\bin\hermes-grok-delegate.ps1" "Task description..."
```

### Direct one-shot (when bridge is not suitable)
```powershell
grok -z "
SYMBIOSIS ESCALATION from Hermes to Grok Build.

Task: <clear description>

Context / previous work:
<paste summary or file references>

Recommended Grok workflow: implement / design / check / best-of-n / review / pptx etc.

After completion, provide clear summary + key file paths.
If long-running execution or gateway delivery is needed afterward, hand back to Hermes.
"
```

### Cross-Device Handoff Language
When the task involves the other machine (Oregon Linux), include:
`[CROSS-DEVICE HANDOFF]`

Example:
```
[CROSS-DEVICE HANDOFF: Windows → Oregon]

Task: ...
Use the shared grok-hermes-symbiosis repo for any artifacts.
Coordinate status in the joint Slack channel.
```

## Recommended Grok Build Capabilities

- `implement` (with reviewers) for new features/refactors
- `design` for architecture and design docs
- `check` for independent verification
- `best-of-n` for exploring multiple approaches
- `review` for code review
- `pptx` / `xlsx` / `docx` for professional polished output
- Plan mode for genuinely ambiguous work

## Windows-Specific Notes

- Grok Build binary is usually at `C:\Users\<you>\.grok\bin\grok.exe`
- Use the `hermes-grok-delegate.ps1` script in `~/bin` for convenience.
- After delegation, the results will appear in the working directory or as specified in the prompt.
- The bridge scripts automatically include cross-device context when used.

## After Delegation

- Review the output from Grok Build.
- If the task requires long execution, persistence, or delivery via gateway/kanban, hand control back to Hermes.
- Commit important artifacts to the shared repo when appropriate.

## Related

- Reciprocal skill on this machine: `hermes` skill (for delegating from Grok Build to Hermes)
- Cross-device coordination: Use the shared Slack channel + `cross-device` patterns
- Shared repo: `C:\Users\spear\grok-hermes-symbiosis`

<!-- Edited: 2026-05-27 14:10 | Device: Windows | By: Grok --> Added Behavioral Prime Directives section (Bing Bang Boom + Linux Turn Indicator) to address the hygiene gap flagged by Linux in the post-21479fb updates. Signature per prime directive. Keep er goinnnn. Boom! -->
