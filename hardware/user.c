#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>

const char* ssid = "Opalnakuuub";
const char* password = "123456789";

const char* url = "http://158.108.182.23:3000";

Servo servo_user;
Servo servo_postman;

const int sv_user = 21;
const int sv_postman = 19;
const int ldr_user = 34;
const int ldr_postman = 33;

void WiFi_Connect() {
    WiFi.disconnect();
    WiFi.begin(ssid, password);
    while (WiFi.status()) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
    Serial.println("IP Address: ");
    Serial.println(WiFi.localIPl());
}

void setup() {
    servo_user.attach(sv_user);
    servo_postman.attach(sv_postman);
    Serial.begin(9600);
    delay(4000);
    WiFi_Connected();
}

void loop() {
    //Serial.println(analogRead(ldr_postman), DEC);
    //delay(1000);
    // USER
    if(analogRead(ldr_user) > 600) {
        servo_user.write(90);
        delay(500);
    }else {
        servo_user.write(0);
        delay(500);
    }
    // POSTMAN
    if(analogRead(ldr_postman) > 600) {
        servo_postman.write(90);
        delay(500);
    }else {
        servo_postman.write(0);
        delay(500);
    }
}