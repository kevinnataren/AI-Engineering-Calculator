# AI Engineering Calculator

A custom handheld engineering calculator built around a Raspberry Pi, ESP32, camera, and AI.

The goal of this project is to create a portable calculator-style device that combines traditional scientific calculator functions with engineering reference tools, AI assistance, and camera-based problem solving.

## Current Features

- Scientific calculator
- Degree and radian modes
- Engineering formula library
- AI engineering assistant over Wi-Fi
- Raspberry Pi camera problem scanning
- AI image analysis and step-by-step solutions

## Calculator Modes

### CALC
Offline scientific calculator supporting common mathematical operations including:

- Addition, subtraction, multiplication, division
- Trigonometric functions
- Logarithms
- Square roots
- Powers
- Pi
- Degree and radian modes

### AI
Allows the user to type engineering or math questions and receive short, readable, step-by-step solutions.

Responses are formatted for a small calculator display using:

- Given
- Formula
- Convert
- Substitute
- Solve
- Answer

### CAMERA
Uses a Raspberry Pi camera to capture a math or engineering problem.

The image is sent to an AI vision model, which reads the problem and returns a structured solution on the calculator interface.

### ENGINEERING
Offline engineering formula library containing sections for:

- Circuits
- Electronics
- Signals
- Electromagnetics
- RF and Antennas
- Probability
- Engineering constants

## Hardware

Current prototype:

- Raspberry Pi 5
- Raspberry Pi Camera
- ESP32
- Monitor
- Keyboard and mouse

Planned final hardware:

- Raspberry Pi Zero 2 W or similar compact computer
- ESP32 keypad controller
- Small LCD
- Physical calculator keypad
- Rechargeable battery
- USB-C charging
- Custom enclosure

## Project Status

| Feature | Status |
|---|---|
| Main interface | ✅ Complete |
| Scientific calculator | ✅ Complete |
| Engineering formulas | ✅ Complete |
| AI mode | ✅ Complete |
| Camera problem solver | ✅ Complete |
| ESP32 keypad | ⏳ Next |
| Small LCD | ⏳ Planned |
| Battery system | ⏳ Planned |
| Custom enclosure | ⏳ Planned |

## System Architecture

```text
                    Wi-Fi / AI API
                          ↑
                          |
Camera ───────────→ Raspberry Pi
                          ↑
                          |
ESP32 ─────────────→ Keypad

Raspberry Pi ──────→ LCD Display
```


## Software

The current software is written primarily in Python.

Main technologies include:

- Python
- Tkinter
- SymPy
- OpenAI API
- Raspberry Pi camera tools
- Multithreading

## Future Development

The next stages of the project will focus on turning the desktop prototype into a fully portable handheld device.

Planned improvements include:

- ESP32 physical keypad
- Small integrated display
- Battery-powered operation
- USB-C charging
- Automatic startup directly into the calculator UI
- Custom calculator enclosure
- Improved engineering tools and formula libraries

## Author

Kevin Nataren

Electrical Engineering student
