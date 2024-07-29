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

    String sAQI  = data.substring(0, data.indexOf("A"));
    String sO3   = data.substring(data.indexOf("A")+1, data.indexOf("B"));
    String sSO2  = data.substring(data.indexOf("B")+1, data.indexOf("C"));
    String sCO   = data.substring(data.indexOf("C")+1, data.indexOf("D"));
    String sNH3  = data.substring(data.indexOf("D")+1, data.indexOf("E"));
    String sNO2  = data.substring(data.indexOf("E")+1, data.indexOf("F"));
    String sPM25 = data.substring(data.indexOf("F")+1, data.indexOf("G"));
    String sPM10 = data.substring(data.indexOf("G")+1, data.indexOf("H"));
    String sTEMP = data.substring(data.indexOf("H")+1, data.indexOf("I"));
    String sHUMD = data.substring(data.indexOf("I")+1, data.indexOf("J"));
    String significant_pollutant = data.substring(data.indexOf("J")+1);
    significant_pollutant.replace("\r", "");
    String areaUID = "a1";
    String moduleID = "m1";
    


    int AQI    = sAQI.toInt();
    float O3   = sO3.toFloat();
    float SO2  = sSO2.toFloat();
    float CO   = sCO.toFloat();
    float NH3  = sNH3.toFloat();
    float NO2  = sNO2.toFloat();
    float PM25 = sPM25.toFloat();
    float PM10 = sPM10.toFloat();
    int TEMP = sTEMP.toInt();
    int HUMD = sHUMD.toInt();

    WiFiClientSecure client;
    client.setInsecure();

    if (!client.connect(host, httpsPort)) {
      Serial.println("Connection failed");
      return;
    }

    StaticJsonDocument<300> jsonDoc;
    jsonDoc["AQI"] = AQI;
    jsonDoc["O3"] = O3;
    jsonDoc["SO2"] = SO2;
    jsonDoc["CO"] = CO;
    jsonDoc["NH3"] = NH3;
    jsonDoc["NO2"] = NO2;
    jsonDoc["PM2.5"] = PM25;
    jsonDoc["PM10"] = PM10;
    jsonDoc["temp"] = TEMP;
    jsonDoc["humd"] = HUMD;
    jsonDoc["significant_pollutant"] = significant_pollutant;
    jsonDoc["areaUID"] = areaUID;
    jsonDoc["moduleID"] = moduleID;

    String jsonString;
    serializeJson(jsonDoc, jsonString);

    String url = "/prod/update-aqi-module-data"; 
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
