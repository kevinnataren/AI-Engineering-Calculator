# AGENTS.md

This repository is the source of truth for the AI Engineering Calculator project.

Before making substantial changes, read:
- `docs/PROJECT_STATE.md`
- `docs/ARCHITECTURE.md`
- `docs/hardware.md`
- `docs/software.md`
- `docs/DECISIONS.md`
- `docs/PCB_PLAN.md`
- `docs/milestones.md`
- `docs/project_log.md`
- `ece361_method.txt` when working on ECE 361 camera solving

Project rules:
1. Preserve tested behavior unless the task explicitly changes it.
2. Keep generic camera solving separate from ECE 361 course-mode behavior.
3. Preserve multi-image camera solving and camera-session memory unless explicitly changed.
4. The final compute target is Raspberry Pi 3 Model A+; Raspberry Pi 5 is development hardware.
5. The display target is the Waveshare 2.8-inch 480x640 portrait touchscreen.
6. The current ESP32-S3 firmware uses a 6x6 keypad matrix with 36 commands.
7. Never assume a power source is safe for the Pi without verifying voltage, current capability, and polarity.
8. PCB mechanical fit and keypad alignment must be verified at 1:1 scale before fabrication.
9. Keep the keypad-contact side of the custom PCB flat where possible.
10. Do not route the Raspberry Pi CSI camera link through PCB Rev 1; use a mechanical ribbon-cable keep-out or slot.
11. Update the matching file under `docs/` when a task changes a project fact, design decision, architecture choice, or milestone.

Before committing Python changes, run:
```bash
python3 -m py_compile main.py
```

If changing ESP32 firmware, verify the PlatformIO project under `esp32_keypad/` builds.

Keep the small-screen UI simple, readable, and dependency-light. Prefer reversible changes and branches for substantial refactors or hardware-interface changes.
