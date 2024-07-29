#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

const int moisture_pin = 32;
const char* ssid = "EA-Project";
const char* password = "projectea";
const char* host = "7l9qpd8im3.execute-api.ap-south-1.amazonaws.com";
const int httpsPort = 443;


void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  String areaUID = "a1";
  String moduleID = "m1";

  float moisture_analog = analogRead(moisture_pin);
  float moisture = ( 100 - ( (moisture_analog/4095.00) * 100 ) );

  WiFiClientSecure client;
    client.setInsecure();

    if (!client.connect(host, httpsPort)) {
      Serial.println("Connection failed");
      return;
    }

    StaticJsonDocument<200> jsonDoc;
    jsonDoc["moisture"] = moisture;
    jsonDoc["areaUID"] = areaUID;
    jsonDoc["moduleID"] = moduleID;

    String jsonString;
    serializeJson(jsonDoc, jsonString);

    String url = "/prod/update-soil-module-data"; 
    client.println("POST " + url + " HTTP/1.1");
    client.println("Host: " + String(host));
    client.println("User-Agent: ESP32");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(jsonString.length());
    client.println();
    client.println(jsonString);
    String error = client.readStringUntil('\n');
    Serial.println(error);
    client.stop();


  delay(5000);
}
