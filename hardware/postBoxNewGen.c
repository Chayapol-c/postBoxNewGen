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

bool get_user, get_postman;

void WiFi_Connect() {
    WiFi.disconnect();
    WiFi.begin(ssid, password);
    if (WiFi.status()) {
       Serial.println("work");
    }else {
      Serial.println("not work");
    }
}

void _get() {
    if(Wifi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(url);
        int httpCode = http.GET();
        if(httpCode == HTTP_CODE_OK) {
            Serial.println(httpCode);
            Serial.print("Lock_user: ");
            Serial.println((bool)JSONGet["Lock_user"]);
            get_user = JSONGet["Lock_user"];
            Serial.print("Lock_postman: ");
            Serial.println((bool)JSONGet["Lock_postman"]);
            get_postman = JSONGet["Lock_postman"];
        }else {
            Serial.println(httpCode);
            Serial.println("ERROR on HTTP Request");
        }
    }else {
        WiFi_Connect();
    }
}

void _post(int sw, bool status) {
    if(WiFi.status() == WL_CONECTED) {
        HTTPCLient http;
        http.begin(url);
        http.addHeader("Content-Type", "application/json");
        if(sw == 0) {
            JSONPost["Lock_user"] = state;
        }else {
            JSONPost["Lock_postman"] = state;
        }
        
        serializeJson(JSONPost, str);
        int httpCode = http.POST(str);

        if(httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            Serial.println(httpCode);
            Serial.println(payload);
        }else {
            Serial.println(httpCode);
            Serial.println("ERROR on HTTP Request");
        }
    }else {
        WiFi_Connect();
    }
}

void setup() {
    servo_user.attach(sv_user);
    servo_postman.attach(sv_postman);
    Serial.begin(9600);
    delay(4000);
    WiFi_Connect();
}

void loop() {
    _get();// Lock_user, Lock_postman
    //Serial.println(analogRead(ldr_postman), DEC);
    //delay(1000);

    // USER
    if(analogRead(ldr_user) > 600) {
        servo_user.write(90); // lock
        delay(500);
        _post(0, true);
        
    }else {
        servo_user.write(0);
        delay(500);
        _post(0, false);
    }
    // POSTMAN
    if(analogRead(ldr_postman) > 600) {
        servo_postman.write(90);
        delay(500);
        _post(1, true);
    }else {
        servo_postman.write(0);
        delay(500);
        _post(1, false);
    }
}