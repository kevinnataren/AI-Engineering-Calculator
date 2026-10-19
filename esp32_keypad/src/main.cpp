#include <Arduino.h>

struct Key {
    int pin;
    const char* message;
    bool lastState;
};

Key keys[] = {
    {4,  "KEY:7",     HIGH},
    {5,  "KEY:8",     HIGH},
    {6,  "KEY:9",     HIGH},
    {7,  "KEY:DIV",   HIGH},

    {8,  "KEY:4",     HIGH},
    {9,  "KEY:5",     HIGH},
    {10, "KEY:6",     HIGH},
    {11, "KEY:MUL",   HIGH},

    {12, "KEY:1",     HIGH},
    {13, "KEY:2",     HIGH},
    {14, "KEY:3",     HIGH},
    {15, "KEY:SUB",   HIGH},

    {16, "KEY:0",     HIGH},
    {17, "KEY:DOT",   HIGH},
    {18, "KEY:ADD",   HIGH},
    {21, "KEY:ENTER", HIGH},

    {38, "KEY:CLEAR", HIGH},
    {39, "KEY:BACK",  HIGH},
    {40, "KEY:LPAREN",HIGH},
    {41, "KEY:RPAREN",HIGH},
    {42, "KEY:SQRT",  HIGH},
    {47, "KEY:POW",   HIGH}
};

const int keyCount = sizeof(keys) / sizeof(keys[0]);

void setup() {
    Serial.begin(115200);

    for (int i = 0; i < keyCount; i++) {
        pinMode(keys[i].pin, INPUT_PULLUP);
    }

    delay(1000);
    Serial.println("ESP32-S3 22-KEY TEST READY");
}

void loop() {
    for (int i = 0; i < keyCount; i++) {
        bool currentState = digitalRead(keys[i].pin);

        if (keys[i].lastState == HIGH && currentState == LOW) {
            Serial.println(keys[i].message);
        }

        keys[i].lastState = currentState;
    }

    delay(20);
}
