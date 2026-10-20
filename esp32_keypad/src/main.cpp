#include <Arduino.h>

const int ROWS = 6;
const int COLS = 6;

int rowPins[ROWS] = {4, 5, 6, 7, 8, 9};
int colPins[COLS] = {10, 11, 12, 13, 14, 15};

const char* keyMap[ROWS][COLS] = {
    {"KEY:7",    "KEY:8",      "KEY:9",      "KEY:DIV",    "KEY:CLEAR",  "KEY:BACK"},
    {"KEY:4",    "KEY:5",      "KEY:6",      "KEY:MUL",    "KEY:LPAREN", "KEY:RPAREN"},
    {"KEY:1",    "KEY:2",      "KEY:3",      "KEY:SUB",    "KEY:SQRT",   "KEY:POW"},
    {"KEY:0",    "KEY:DOT",    "KEY:ADD",    "KEY:ENTER",  "KEY:SIN",    "KEY:COS"},
    {"KEY:TAN",  "KEY:LOG",    "KEY:LN",     "KEY:ANGLE",  "KEY:PI",     "KEY:E"},
    {"KEY:HOME", "KEY:AI",     "KEY:CAMERA", "KEY:ENG",    "KEY:UP",     "KEY:DOWN"}
};

bool stableState[ROWS][COLS] = {false};
bool lastReading[ROWS][COLS] = {false};

unsigned long lastChangeTime[ROWS][COLS] = {0};

const unsigned long debounceDelay = 50;

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
    Serial.println("ESP32-S3 6x6 MATRIX READY");
}

void loop() {
    for (int r = 0; r < ROWS; r++) {

        digitalWrite(rowPins[r], LOW);
        delayMicroseconds(50);

        for (int c = 0; c < COLS; c++) {

            bool reading = (digitalRead(colPins[c]) == LOW);

            if (reading != lastReading[r][c]) {
                lastChangeTime[r][c] = millis();
                lastReading[r][c] = reading;
            }

            if (
                millis() - lastChangeTime[r][c] > debounceDelay &&
                reading != stableState[r][c]
            ) {
                stableState[r][c] = reading;

                if (stableState[r][c]) {
                    Serial.println(keyMap[r][c]);
                }
            }
        }

        digitalWrite(rowPins[r], HIGH);
    }
}
