#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

const char* ssid = "EA-Project";
const char* password = "projectea";
const char* host = "7l9qpd8im3.execute-api.ap-south-1.amazonaws.com";
const int httpsPort = 443;


void setup() {
  Serial.begin(9600);  
  Serial2.begin(9600, SERIAL_8N1, 16, 17);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}


void loop() {
  if(Serial2.available() > 0)
  {
    String data = Serial2.readStringUntil('\n');

    String spH  = data.substring(0, data.indexOf("A"));
    String sturbidity   = data.substring(data.indexOf("A")+1, data.indexOf("B"));
    String sTDS = data.substring(data.indexOf("B")+1);
    sTDS.replace("\r", "");
    String areaUID = "a1";
    String moduleID = "m1";

    float pH    = spH.toFloat();
    float turbidity   = sturbidity.toFloat();
    float TDS  = sTDS.toFloat();

    WiFiClientSecure client;
    client.setInsecure();

    if (!client.connect(host, httpsPort)) {
      Serial.println("Connection failed");
      return;
    }

    StaticJsonDocument<300> jsonDoc;
    jsonDoc["pH"] = pH;
    jsonDoc["turbidity"] = turbidity;
    jsonDoc["TDS"] = TDS;
    jsonDoc["areaUID"] = areaUID;
    jsonDoc["moduleID"] = moduleID;

    String jsonString;
    serializeJson(jsonDoc, jsonString);

    String url = "/prod/update-water-module-data"; 
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

  }
}
