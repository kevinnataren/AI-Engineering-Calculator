#include <Arduino.h>

const int ROWS = 4;
const int COLS = 4;

int rowPins[ROWS] = {4, 5, 6, 7};
int colPins[COLS] = {8, 9, 10, 11};

const char* keyMap[ROWS][COLS] = {
    {"KEY:7", "KEY:8", "KEY:9", "KEY:DIV"},
    {"KEY:4", "KEY:5", "KEY:6", "KEY:MUL"},
    {"KEY:1", "KEY:2", "KEY:3", "KEY:SUB"},
    {"KEY:0", "KEY:DOT", "KEY:ADD", "KEY:ENTER"}
};

bool lastState[ROWS][COLS] = {false};

void setup() {
    Serial.begin(115200);

    for (int r = 0; r < ROWS; r++) {
        pinMode(rowPins[r], OUTPUT);
        digitalWrite(rowPins[r], HIGH);
    }

    for (int c = 0; c < COLS; c++) {
        pinMode(colPins[c], INPUT_PULLUP);
    }

    delay(1000);
    Serial.println("ESP32-S3 MATRIX KEYPAD READY");
}

void loop() {
    for (int r = 0; r < ROWS; r++) {

        digitalWrite(rowPins[r], LOW);

        for (int c = 0; c < COLS; c++) {
            bool pressed = (digitalRead(colPins[c]) == LOW);

            if (pressed && !lastState[r][c]) {
                Serial.println(keyMap[r][c]);
            }

            lastState[r][c] = pressed;
        }

        digitalWrite(rowPins[r], HIGH);
    }

    delay(20);
}
