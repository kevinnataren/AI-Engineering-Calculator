# AI Engineering Calculator

A custom handheld engineering calculator built around a Raspberry Pi, ESP32-S3, camera, physical keypad, touchscreen display, and AI.

The goal of this project is to create a portable calculator-style device that combines traditional scientific calculator functions with engineering reference tools, AI assistance, and camera-based problem solving.

## Current Features

- Scientific calculator
- Degree and radian modes
- Offline engineering formula library
- AI engineering assistant over Wi-Fi
- Camera-based engineering problem solving
- Up to 3 photos for one continuous problem
- ESP32-S3 6x6 physical keypad
- Physical navigation and scrolling
- Waveshare 2.8-inch 480x640 touchscreen
- Fullscreen calculator interface
- Automatic startup
- Automatic ESP32 serial reconnection

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
Uses the Raspberry Pi camera to capture math or engineering problems.

Up to three photos can be captured for one continuous problem. The images are sent together to an AI vision model, which reads the complete problem and returns a structured solution on the calculator interface.

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

Current development hardware:

- Raspberry Pi 5
- Raspberry Pi Camera Module 3 Wide NoIR
- ESP32-S3
- Waveshare 2.8-inch 480x640 HDMI LCD

Final handheld hardware:

- Raspberry Pi 3 Model A+
- ESP32-S3 keypad controller
- Waveshare 2.8-inch 480x640 HDMI LCD
- Raspberry Pi Camera Module 3 Wide NoIR
- Physical calculator keypad
- Rechargeable battery system
- USB-C charging
- Calculator-style donor enclosure

## Project Status

| Feature | Status |
|---|---|
| Main interface | Complete |
| Scientific calculator | Complete |
| Engineering formulas | Complete |
| AI mode | Complete |
| Multi-image camera solver | Complete |
| ESP32-S3 6x6 keypad firmware | Complete |
| Physical keypad integration | Complete |
| Waveshare display integration | Complete |
| Fullscreen UI optimization | Complete |
| Automatic startup | Complete |
| ESP32 automatic reconnect | Complete |
| Raspberry Pi 3 A+ deployment | Tested |
| Portable battery system | In progress |
| Final donor enclosure | Pending hardware |

## System Architecture

Camera -> Raspberry Pi 3 A+ -> Waveshare LCD

6x6 Physical Keypad -> ESP32-S3 -> USB Serial -> Raspberry Pi 3 A+

Raspberry Pi 3 A+ -> Wi-Fi -> AI API

## Software

The current software is written primarily in Python.

Main technologies include:

- Python
- Tkinter
- SymPy
- OpenAI API
- Raspberry Pi camera tools
- PySerial
- Multithreading
- PlatformIO / Arduino framework for ESP32-S3 firmware

## Raspberry Pi Deployment

The project includes setup_pi.sh and requirements.txt for installing the required Raspberry Pi system packages, creating the Python virtual environment, and installing Python dependencies.

The calculator is configured to launch automatically when the Raspberry Pi desktop starts.

## Current Development Stage

The core software and electronics interfaces are operational.

Remaining work is focused on:

- Portable power integration
- Final physical keypad construction
- Internal component placement
- Donor enclosure modification
- Final handheld assembly and testing

## Author

Kevin Nataren

Electrical Engineering student
