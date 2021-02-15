#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Servo.h>

const char* ssid = "Opalnakuuub";
const char* password = "123456789";

const char* url = "http://158.108.182.23:3000";

int ldr = 32;
int sv_user = 33;

Servo servo_user;

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
    servo_user.attach(sv_user);
    Serial.begin(9600);
    delay(4000);
    WiFi_Connect();
}

void _get() {
    if(WiFi.status() == WL_CONNECTED) {
        HTTPClient http;

        http.begin(url);
        int httpCode = http.GET();
        if(httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            DeserilizationError err = deserializeJson(JSONGet, payload);
            if(err) {
                Serial.print(F("deserializeJson() failed with code "));
                Serial.println(err.c_str());
            }else {
                Serial.println(httpCode);
                Serial.print("statusUser: ");
                Serial.println((bool)JSONGet["statusUser"]);
            }
        }else {
            Serial.println(httpCode);
            Serial.println("ERROR on HTTP Request");
        }
    }else {
        WiFi_Connect();
    }
}

void loop() {
    _get();
    if(JSONGet["statusUser"]) {
        for(int i=0; i<=90; i++) {
            servo_user.write(i);
            delay(50);// wait for 50 millisecond(s).
        }
    }
    if(analogRead(ldr) < 400) {
        for(int i=90; i>=0; i--) {
            servo_user.write(i);
            delay(50);// wait for 50 millisecond(s).
        }
        JSONGet["statusUser"] = false;
    }
}