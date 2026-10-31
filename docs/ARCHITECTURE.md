# System Architecture

## High-level data flow

```text
TI-83 Keys
   ↓
Rubber membrane
   ↓
Custom keypad PCB
   ↓
ESP32-S3
   ↓ serial / UART
Raspberry Pi 3 Model A+
   ├─ Tkinter calculator UI
   ├─ Scientific calculator logic
   ├─ Engineering formula library
   ├─ AI text requests
   ├─ Camera solver
   └─ ECE 361 course-method solver
   ↓
Waveshare 2.8-inch 480x640 touchscreen

Raspberry Pi Camera Module 3 Wide NoIR
   ↓ CSI
Raspberry Pi 3 Model A+

4xAAA battery compartment
   ↓
5 V buck-boost power stage
   ↓
Raspberry Pi 3 Model A+
   ↓
3.3 V rail / local regulator
   ↓
ESP32-S3
```

## Compute split

### Raspberry Pi 3 Model A+
Owns:
- Main UI
- Calculator mode
- AI mode
- Camera mode
- Engineering formula mode
- Image capture and AI vision request
- ECE 361 method selection and stored method loading
- Display output
- Touchscreen interaction
- Wi-Fi/API communication
- High-level interpretation of physical key events

### ESP32-S3
Owns:
- Physical keypad scanning
- Debouncing
- Emitting key events
- Future battery/board-level sensing if desired

The ESP32 should remain a simple, deterministic input controller. Do not move high-level calculator or AI behavior onto the ESP32 without a strong reason.

## Serial protocol
Current firmware emits simple newline-delimited text messages:

```text
KEY:7
KEY:ENTER
KEY:HOME
KEY:CAMERA
```

This protocol is intentionally simple. Keep backward compatibility if the transport changes from USB serial to UART.

## UI architecture
The application uses a fullscreen Tkinter root window.

Primary modes:
- HOME
- CALC
- AI
- CAMERA
- ENGINEERING

`current_screen` is used for navigation behavior. `active_scroll_widget` is used so physical UP/DOWN keys can scroll the currently relevant text area.

## Camera architecture
CAMERA mode supports up to 3 images for one problem.

```text
Capture image 1
Capture image 2
Capture image 3
      ↓
One AI request containing all images
      ↓
One continuous solution
```

A 15-minute camera-session memory preserves the last camera answer when leaving and returning to CAMERA mode.

## Course-specific solving
GENERAL mode uses the generic engineering-calculator prompt and output style.

ECE 361 mode loads `ece361_method.txt` and prepends course-method instructions so the stored method can override the generic numerical format.

Do not merge these into one undifferentiated prompt. Course-specific behavior must remain explicit and testable.

## Power architecture
The final power path must not connect the battery pack directly to the Raspberry Pi.

Target:

```text
4xAAA pack
   ↓
input protection / switch
   ↓
5 V buck-boost regulator
   ↓
5 V rail to Pi
   ↓
3.3 V regulation where needed
   ↓
ESP32-S3 and low-voltage logic
```

Because 4xAAA can be above or below 5 V, a buck-boost topology is required if the design is intended to support both alkaline and rechargeable AAA cells over their usable discharge ranges.

## PCB partitioning
### Keypad side
Keep flat:
- Exposed key contacts
- Minimal/no components
- Correct geometry for TI rubber membrane

### Component side
Place:
- ESP32-S3 module
- Regulators
- USB/programming connector if used
- Test points
- UART/serial connector or pads
- Power components

### Camera
Do not route the Pi CSI link through Rev 1. Leave a keep-out or physical slot for the camera ribbon to pass directly to the Pi.
