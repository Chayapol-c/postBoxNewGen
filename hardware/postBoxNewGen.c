#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>

const char* ssid = "Opalnakuuub";
const char* password = "123456789";
char str[100];

const int _size = 2 * JSON_OBJECT_SIZE(2);
StaticJsonDocument<_size> JSONGet;
StaticJsonDocument<_size> JSONPost;

const char* url_get = "http://158.108.182.23:3000/status?user=yooo";
const char* url_post = "http://158.108.182.23:3000/status/update";

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
    if(WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(url_get);
        int httpCode = http.GET();
        if(httpCode == HTTP_CODE_OK) {
            String payload = http.getString();
            DeserializationError err = deserializeJson(JSONGet, payload);
            if(!err) {
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
        }
    }else {
        WiFi_Connect();
    }
}

void _post(int sw, bool status) {
    if(WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(url_post);
        http.addHeader("Content-Type", "application/json");
        if(sw == 0) {
            JSONPost["username"] = "yooo";
            JSONPost["Lock_user"] = status;
            JSONPost["Lock_postman"] = get_postman;
        }else {
            JSONPost["username"] = "yooo";
            JSONPost["Lock_postman"] = status;
            JSONPost["Lock_user"] = get_user;
        }
        Serial.println(str);
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
    servo_user.write(90);
    servo_postman.write(90);
    Serial.begin(9600);
    delay(4000);
    WiFi_Connect();
}

void loop() {
    _get();
    Serial.println(analogRead(ldr_postman), DEC);
    delay(1000);
    // POSTMAN
    if(!get_postman) {
        servo_postman.write(0);
    }
    if(analogRead(ldr_postman) > 2500) {
        servo_postman.write(90);//LOCK
        delay(500);
        _post(1, true);
    }
    
    //USER
    if(!get_user) {
        servo_user.write(0);
    }
    if(analogRead(ldr_user) > 2500) {
        servo_user.write(90); // lock
        delay(500);
        _post(0, true);
    }
    delay(5000);
}