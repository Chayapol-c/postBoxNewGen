#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Servo.h>

const char* ssid = "Opalnakuuub";
const char* password = "123456789";

const char* url = "http://158.108.182.23:3000";

int ldr = 32;
int sv_postman = 33;
int sv_user = 34;

Servo servo_postman, servo_user;

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
    pinMode(ldr, INPUT);
    servo_postman.attach(33);
    servo_user.attach(34);  
    Serial.begin(9600);
    delay(4000);
    WiFi_Connect();
}

void loop() {
    
}