#include <Arduino.h>

struct Key {
    int pin;
    const char* message;
    bool lastState;
};

Key keys[] = {
    {4,  "KEY:7",   HIGH},
    {5,  "KEY:8",   HIGH},
    {6,  "KEY:9",   HIGH},
    {7,  "KEY:DIV", HIGH},

    {8,  "KEY:4",   HIGH},
    {9,  "KEY:5",   HIGH},
    {10, "KEY:6",   HIGH},
    {11, "KEY:MUL", HIGH}
};

const int keyCount = sizeof(keys) / sizeof(keys[0]);

void setup() {
    Serial.begin(115200);

    for (int i = 0; i < keyCount; i++) {
        pinMode(keys[i].pin, INPUT_PULLUP);
    }

    delay(1000);
    Serial.println("ESP32-S3 8-KEY TEST READY");
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
