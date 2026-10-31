# Project State

Last consolidated: 2026-10-30

## Goal
Build a handheld AI engineering calculator in a TI-83 Plus-style enclosure that combines scientific calculation, offline engineering references, AI assistance, camera-based problem solving, physical keys, and a small portrait touchscreen.

## Current known-good software baseline
Branch: `phase2-multi-image-camera`
Known-good commit before second-brain work: `67294bd` (`Add ECE 361 professor-method camera mode`)

## Software status
### Complete / working
- Fullscreen Tkinter UI sized for 480x640 portrait display.
- HOME, CALC, AI, CAMERA, and ENGINEERING modes.
- Scientific calculator with arithmetic, trig, logs, roots, powers, pi, e, DEG/RAD.
- Offline engineering formula library for circuits, electronics, signals, electromagnetics, RF/antennas, probability, constants.
- AI text mode.
- Camera problem solving with up to 3 photos treated as one continuous problem.
- CAMERA method selector with GENERAL and ECE 361 modes.
- ECE 361 course method library stored in `ece361_method.txt`.
- Camera answer/session memory retained for 15 minutes.
- Friendly camera/network/API error handling.
- ESP32-S3 serial worker with automatic reconnect.
- Physical navigation support for HOME, AI, CAMERA, ENGINEERING, UP, DOWN, BACK, ENTER, calculator keys, and angle mode.
- Smart BACK behavior based on current screen.
- Auto-start on Raspberry Pi desktop startup.
- Raspberry Pi deployment scripts and requirements file.

### Tested hardware behavior
- Waveshare 2.8-inch 480x640 touchscreen works with the calculator UI.
- LCD and touch still worked after temporarily disconnecting/reconnecting the display flex cables from the Waveshare controller board.
- Raspberry Pi 3 Model A+ can physically fit in the TI-83 Plus enclosure in at least one orientation where the back shell can close.
- ESP32-S3 development board is too bulky to fit cleanly in the current enclosure layout.

## ESP32 keypad firmware
Location: `esp32_keypad/`
Current matrix: 6 rows x 6 columns = 36 commands.
Current row GPIOs: 4, 5, 6, 7, 8, 9.
Current column GPIOs: 10, 11, 12, 13, 14, 15.
Current firmware emits `KEY:<name>` messages over serial at 115200 baud.

Current logical mapping:
- Row 0: 7, 8, 9, DIV, CLEAR, BACK
- Row 1: 4, 5, 6, MUL, LPAREN, RPAREN
- Row 2: 1, 2, 3, SUB, SQRT, POW
- Row 3: 0, DOT, ADD, ENTER, SIN, COS
- Row 4: TAN, LOG, LN, ANGLE, PI, E
- Row 5: HOME, AI, CAMERA, ENG, UP, DOWN

## Camera / ECE 361
`ece361_method.txt` contains class-method notes and solution patterns for:
- Coulomb law and continuous charge
- Gauss law, dielectrics, boundary conditions
- Poisson/Laplace and capacitors
- Conductivity/current/resistance
- Magnetostatics/Ampere law
- Uniform plane waves
- Lossy waves, attenuation, dispersion
- Poynting vector/power
- Polarization

ECE 361 mode must prioritize stored course method, notation, equation order, and compact equation-driven style over the generic camera solution format.

## Final hardware direction
### Enclosure
- TI-83 Plus donor shell.
- Original TI keypad plastic keys and rubber membrane should be reused if practical.
- Original TI motherboard is not intended to remain as the compute platform.

### Compute
- Final board: Raspberry Pi 3 Model A+.
- Development board: Raspberry Pi 5.

### Display
- Waveshare 2.8-inch HDMI LCD, 480x640 portrait, capacitive touch.
- LCD can be separated from the blue Waveshare controller PCB and reconnected successfully.
- Final mechanical layout should keep the LCD at the front and relocate the controller PCB where space allows.

### Camera
- Raspberry Pi Camera Module 3 Wide NoIR / IMX708 wide NoIR.
- Direct CSI ribbon to Raspberry Pi is preferred.

### Keypad / controller
- Current ESP32-S3 dev board is proven in software but too bulky for the final enclosure.
- Final direction is a custom PCB replacing or copying the original TI keypad PCB geometry.
- Custom board should integrate keypad contacts and preferably an ESP32-S3 module directly.

### Power
Chosen design direction: retain the original 4xAAA rear battery compartment and use a regulated 5 V power system for the Raspberry Pi.

Important: 4xAAA can be above or below 5 V depending on chemistry/state of charge, so the final design requires a buck-boost stage rather than a simple direct connection.

AAA current capability and runtime are not yet validated. This is an open engineering risk.

A previously purchased 7.4 V lithium pack and a 3.7 V 18650 cell exist but are not the chosen final power architecture at this time.

## Custom PCB direction
Use KiCad for design and JLCPCB for fabrication.

Rev 1 concept:
- Board outline and mounting holes based on original TI motherboard.
- Exposed keypad contacts aligned to original rubber membrane.
- ESP32-S3 module on board.
- Keypad matrix traces.
- UART or serial connection to Raspberry Pi.
- Battery input from original AAA contacts.
- 5 V high-current buck-boost power stage, initially possibly implemented with a proven module mounted to the PCB rather than a scratch switching design.
- 3.3 V rail for ESP32.
- Camera ribbon keep-out/slot rather than routing CSI through Rev 1.
- Test points for BAT, 5V, 3V3, GND, TX, RX.
- Components on the side opposite the keypad contacts where possible.

## Open questions / risks
- Exact TI board dimensions, mounting-hole coordinates, and keypad-contact coordinates still need to be measured accurately.
- Exact PCB thickness should match or be compatible with the original TI board.
- AAA batteries may not sustain the Pi/display/camera current under peak load; must be measured and tested.
- Final choice of buck-boost converter/module is not locked.
- Final ESP32 module/package is not locked.
- Final method for connecting the custom keypad PCB to the Pi is not locked; UART is preferred for simplicity.
- Final placement of Waveshare controller PCB and custom PCB inside the shell remains a mechanical task.

## Immediate next phase
1. Capture accurate mechanical dimensions from the original TI motherboard and shell.
2. Build a KiCad mechanical template first.
3. Verify the PCB outline and keypad positions with a 1:1 print.
4. Add keypad matrix and ESP32 architecture.
5. Add the power section only after the mechanical design is validated.
6. Generate Gerbers and drill files for JLCPCB only after ERC/DRC and 1:1 fit checks pass.
