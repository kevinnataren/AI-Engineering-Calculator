# Codex Workflow

## Why this exists
The project now spans software, embedded firmware, camera behavior, mechanical enclosure work, power electronics, and custom PCB design. Chat history is not the authoritative memory. The repository is.

## Starting a new Codex task
At the beginning of a substantial task, Codex should read:
1. `AGENTS.md`
2. `docs/PROJECT_STATE.md`
3. The task-specific doc:
   - software -> `docs/software.md`
   - hardware/mechanical -> `docs/hardware.md`
   - PCB -> `docs/PCB_PLAN.md`
   - architecture -> `docs/ARCHITECTURE.md`
   - prior choices -> `docs/DECISIONS.md`
4. The relevant source files.

For ECE 361 camera work, also read `ece361_method.txt`.

## Task format
Use focused tasks. Good examples:
- "Add UART support between the ESP32-S3 and Raspberry Pi while preserving the current KEY protocol."
- "Create the KiCad project skeleton and mechanical PCB outline from the measured TI-83 dimensions."
- "Refactor camera session state without changing the 15-minute behavior."

Avoid vague tasks such as:
- "Finish the calculator."
- "Make the PCB."

## Branching
Use a dedicated branch for substantial changes.

Suggested naming:
```text
software/<feature>
firmware/<feature>
pcb/<feature>
hardware/<feature>
docs/<feature>
```

Examples:
```text
pcb/ti83-mechanical-template
firmware/uart-transport
software/battery-status
```

## Definition of done
A task is not complete until:
- Relevant code/build checks pass.
- Hardware assumptions are stated explicitly.
- The matching project-memory doc is updated if facts or decisions changed.
- No secret keys or credentials are committed.
- The change is committed with a descriptive message.

## Software checks
For Python changes:
```bash
python3 -m py_compile main.py
```

Run additional focused tests when behavior changed.

## Firmware checks
For ESP32 changes, build the PlatformIO project before completion.

Where hardware is available, also confirm the expected serial messages on the real ESP32.

## PCB checks
Before ordering:
- ERC.
- DRC.
- 1:1 paper fit test.
- Mounting-hole alignment.
- Keypad-contact alignment.
- Enclosure/component-height check.
- Power review.
- Gerber/drill inspection.

## Decision handling
When a task discovers that an existing decision is wrong, do not silently work around it.

Update `docs/DECISIONS.md` with:
- old assumption,
- new decision,
- why it changed,
- what downstream parts are affected.

## Project-state handling
`docs/PROJECT_STATE.md` should describe what is true now, not the entire history.

`docs/project_log.md` is where dated historical milestones and experiments belong.

## Suggested Codex prompt pattern
```text
Read AGENTS.md and docs/PROJECT_STATE.md first.
Then read <task-specific files>.

Goal:
<one concrete outcome>

Constraints:
<what must not change>

Validation:
<commands/tests that must pass>

Update the relevant docs if the task changes a project fact or decision.
```

## Example PCB prompt
```text
Read AGENTS.md, docs/PROJECT_STATE.md, docs/ARCHITECTURE.md,
docs/DECISIONS.md, and docs/PCB_PLAN.md.

Create the first KiCad mechanical template for the TI-83 Plus replacement PCB.
Do not add the power circuit yet.
Use the measured board dimensions and mounting-hole coordinates I provide.
Add the board outline, mounting holes, mechanical keep-outs, and placeholders for keypad contact centers.

Before finishing, run the appropriate KiCad checks available in the environment and update docs/PROJECT_STATE.md with the new PCB status.
```

## Principle
Codex should leave the repository easier for the next task to understand than it found it.
