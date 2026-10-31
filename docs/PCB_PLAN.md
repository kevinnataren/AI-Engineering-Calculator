# PCB Plan

## Goal
Design a custom PCB that replaces the functional role of the original TI-83 Plus keypad motherboard while integrating the keypad interface, compact ESP32-S3 control, power distribution, and clean connections to the Raspberry Pi.

## Rev 1 priorities
Rev 1 should prove, in this order:
1. Mechanical fit.
2. Keypad alignment and reliable key detection.
3. ESP32-S3 integration and Pi communication.
4. Safe regulated power distribution.
5. Serviceability and test access.

Do not optimize for minimum size or maximum integration before these are proven.

## Mechanical reference
Use the original TI motherboard and enclosure as the dimensional reference.

Required measurements:
- Overall PCB outline.
- PCB thickness.
- Mounting-hole diameters.
- Mounting-hole coordinates.
- Corner radii/notches.
- Key-contact center coordinates.
- Key-contact diameters/shape.
- Internal plastic posts and no-go areas.
- LCD/controller keep-outs.
- Raspberry Pi keep-out.
- Camera-ribbon path.
- AAA battery-contact locations.

Preferred capture method:
- Flatbed scan at high resolution with a ruler or known scale reference.
- If unavailable, straight-down orthographic photo with a ruler and minimal perspective distortion.

## KiCad project structure
Suggested directory:

```text
pcb/
  AI_Engineering_Calculator.kicad_pro
  AI_Engineering_Calculator.kicad_sch
  AI_Engineering_Calculator.kicad_pcb
  footprints/
  mechanical/
  fabrication/
```

## Board outline
Create the real enclosure-compatible outline on `Edge.Cuts`.

Use exact coordinates. Do not eyeball the shape from a phone photo.

## Mounting holes
Place mounting holes before electronics. Use them as the mechanical coordinate reference for the rest of the board.

## Keypad contacts
Create a reusable custom footprint representing one TI rubber-key contact.

Requirements:
- Two isolated conductive electrode sets per key.
- Conductive rubber pill bridges the electrodes when pressed.
- Contact surface must be exposed from solder mask.
- Prefer a flat finish suitable for repeated rubber contact.
- Match original TI contact size and location as closely as possible.

Keep the membrane-facing PCB side flat and free of tall components.

## Keypad matrix
Current logical firmware architecture is 6x6.

Current nets can start as:
```text
ROW0 ROW1 ROW2 ROW3 ROW4 ROW5
COL0 COL1 COL2 COL3 COL4 COL5
```

Do not assume the final physical TI key arrangement must exactly match the current logical row/column geometry. The PCB can route physical key locations into the logical matrix.

## ESP32-S3
Preferred direction: integrated ESP32-S3 module rather than the current development board.

Minimum considerations:
- 3.3 V rail.
- Decoupling close to the module.
- EN/reset support.
- BOOT/program support.
- Programming/debug access.
- Antenna keep-out if using a module with onboard antenna.
- No copper/components under the antenna keep-out.

## Pi communication
Preferred final link: UART.

Keep the existing newline-delimited key protocol where possible:
```text
KEY:7
KEY:ENTER
KEY:AI
```

Expose test pads or a small connector for:
- TX
- RX
- GND

## Camera
For Rev 1:
- Do not pass CSI signals through the custom PCB.
- Add a mechanical slot or keep-out so the Pi camera ribbon can pass directly to the Raspberry Pi.

## Power
### Input
Original 4xAAA battery compartment.

### Requirement
Provide a stable 5 V rail suitable for the Raspberry Pi despite battery voltage moving above and below 5 V.

### Rev 1 strategy
Prefer mounting a proven high-current 5 V buck-boost module to the PCB rather than designing the switching converter from scratch.

### Validation needed before lock
- Measure actual Pi + display idle current.
- Measure camera-active current.
- Measure Wi-Fi/AI-use current.
- Measure worst observed transient/peak current.
- Test alkaline AAA pack under load.
- Test rechargeable NiMH AAA pack if that chemistry is intended to be supported.
- Measure voltage sag and practical runtime.

If AAA cells cannot reliably support the load, revisit D009 in `DECISIONS.md` rather than forcing an unsafe design.

## 3.3 V rail
ESP32-S3 requires a suitable 3.3 V supply. Do not assume the Pi 3.3 V rail is automatically the best source for the final board; evaluate current budget and startup behavior.

## Test points
At minimum expose:
- BAT+
- GND
- 5V
- 3V3
- ESP_TX
- ESP_RX
- EN
- BOOT

## Routing guidance
- Keypad/signal traces can be narrow conventional signal traces.
- Battery and 5 V high-current routes should be short and wide, preferably with copper pours where practical.
- Use a ground plane while respecting the ESP32 antenna keep-out.
- Keep switching regulator high-current loops compact.
- Separate noisy switching-power paths from sensitive RF/antenna regions.

## Silkscreen
Useful labels:
- AI ENGINEERING CALCULATOR
- PCB REV 1
- BAT+
- BAT-
- 5V
- 3V3
- GND
- TX
- RX
- BOOT
- RESET
- test-point names

## Validation gates before ordering
Do not generate a fabrication order until all are true:
- Schematic ERC reviewed.
- PCB DRC reviewed.
- No unintended unconnected nets.
- Board outline checked against real shell.
- Mounting holes checked against real shell.
- 1:1 paper print tested physically.
- Every intended keypad contact aligns with the rubber membrane.
- Camera ribbon path checked.
- Pi/display/controller keep-outs checked.
- Component heights checked against case depth.
- Power architecture reviewed and current assumptions documented.

## Fabrication output
For JLCPCB generate:
- Gerbers.
- Excellon drill files.

If using assembly service, also generate:
- BOM.
- Component placement / CPL file.

A PDF is useful for 1:1 physical checking but is not the manufacturing source.

## Rev 2 candidates
After Rev 1 is proven:
- Integrate the buck-boost converter directly onto the PCB.
- Add battery monitoring.
- Add a dedicated safe-shutdown/power-control circuit.
- Revisit full TI keypad mapping beyond the current 36-command logical map.
- Improve connector placement based on real assembly experience.
