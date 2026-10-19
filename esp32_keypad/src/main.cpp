#include <Arduino.h>

struct Key {
    int pin;
    const char* message;
    bool lastState;
};

Key keys[] = {
    {4, "KEY:7",   HIGH},
    {5, "KEY:8",   HIGH},
    {6, "KEY:9",   HIGH},
    {7, "KEY:DIV", HIGH}
};

const int keyCount = sizeof(keys) / sizeof(keys[0]);

void setup() {
    Serial.begin(115200);

    for (int i = 0; i < keyCount; i++) {
        pinMode(keys[i].pin, INPUT_PULLUP);
    }

    delay(1000);
    Serial.println("ESP32-S3 4-KEY TEST READY");
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
