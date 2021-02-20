#include <ESP32Servo.h>

Servo servo_send;

const int sv_send = 18;

void setup() {
    servo_send.attach(sv_send);
    servo_send.write(0);
    Serial.begin(9600);
    delay(1000);
}

void loop() {
    servo_send.write(360);
}