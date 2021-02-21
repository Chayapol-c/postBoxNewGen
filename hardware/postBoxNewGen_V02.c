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

const char* url_get = "http://158.108.182.23:3001/status?user=yooo";
const char* url_post = "http://158.108.182.23:3001/status/update";

Servo servo_user;
Servo servo_postman;
Servo myservo;

const int sv_user = 21;
const int sv_postman = 19;
const int sv_my = 22;
const int ldr_postman = 34;

int check = 1;

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

void _post(bool status) {
    if(WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(url_post);
        http.addHeader("Content-Type", "application/json");        
        JSONPost["username"] = "yooo";
        JSONPost["Lock_postman"] = status;
        JSONPost["Lock_user"] = get_user;
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
    myservo.attach(sv_my);
    servo_user.write(90);
    servo_postman.write(90);
    myservo.write(90);
    Serial.begin(230400);
    delay(4000);
    WiFi_Connect();
}

void loop() {
    _get();
    delay(1000);
    Serial.println(analogRead(ldr_postman), DEC);
    Serial.println(check);
    delay(1000);
    // POSTMAN
    servo_postman.attach(sv_postman);
    if(!get_postman) {
        check = 0;
        Serial.print("in: ");
        Serial.println(check);
        delay(100);
        servo_postman.write(0);
        delay(100);
    }
    if(analogRead(ldr_postman) > 2200 && check == 0) {
        check = 1;
        servo_postman.write(90);//auto LOCK
        delay(15);
        myservo.write(180);
        delay(2200);
        myservo.write(0);
        delay(2200);
        myservo.detach();
        delay(5000);
        _post(true);
        delay(100000); 
    }
    
    //USER
    if(!get_user) {
        servo_user.write(0);
        delay(15);
    }else {
        servo_user.write(90);
        delay(15);
        
    }
    
    delay(5000);
    
}