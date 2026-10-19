#include <Arduino.h>

const int TEST_KEY = 4;

bool lastState = HIGH;

void setup() {
    Serial.begin(115200);

    pinMode(TEST_KEY, INPUT_PULLUP);

    delay(1000);
    Serial.println("ESP32-S3 KEYPAD READY");
}

void loop() {
    bool currentState = digitalRead(TEST_KEY);

    if (lastState == HIGH && currentState == LOW) {
        Serial.println("KEY:7");
    }

    lastState = currentState;
    delay(20);
}
