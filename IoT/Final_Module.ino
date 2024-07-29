#include "MQ131.h"
#include "MQ135.h"
#include "DHT.h"
#include <Wire.h>


#define MQ9pin A2  
#define MQ135pin A3                   


DHT dht;
MQ135 gasSensor = MQ135(MQ135pin);


float GasFactor = 24.57143;
int GasSensorValue = 0;
int measurePin = A0; 
int ledPower = 4;   

int samplingTime = 280;
int deltaTime = 40;
int sleepTime = 9680;

float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;

double AQI = 0;


const int analogInPin = A5;  
const int resValue = 9700;  
const float Vref = 1.1;  
const long int cOff = 68286; 
const float Sf = 2.11; 
const int extraBit = 256; 
long int sensorValue = 0;        
float currentValue = 0; 


void setup() 
{

  Serial.begin(9600);
  delay(3000);
  pinMode(ledPower,OUTPUT);
  dht.setup(2);
  MQ131.begin(3,A1, LOW_CONCENTRATION, 1000000);
  //MQ131.calibrate();
}

void loop() 
{
  AQI = 0.00;

  delay(dht.getMinimumSamplingPeriod());	                     /* Delay of amount equal to sampling period */	
  float humidity = dht.getHumidity();	                        /* Get humidity value */
  float temperature = dht.getTemperature();	                 /* Get temperature value */
  String significantPollutant = "";


  double ppm = gasSensor.getPPM();
  delay(1000);
  double NH3_val = ppm*0.4;

  if(NH3_val>=0.00 && NH3_val <= 200.00)
  {
    double NH3_SI = ((50-0)/(200-0)*(NH3_val-0))+0;
    if(NH3_SI >= AQI)
    {
      AQI = NH3_SI;
      significantPollutant = "NH3";
    }
  }
  else if(NH3_val>=201.00 && NH3_val <= 400.00)
  {
    double NH3_SI = ((100-50)/(400-200)*(NH3_val-200))+50;
    if(NH3_SI >= AQI)
    {
      AQI = NH3_SI;
      significantPollutant = "NH3";
    }
  }
  else if(NH3_val>=401.00 && NH3_val <= 800.00)
  {
    double NH3_SI = ((200-100)/(800-400)*(NH3_val-400))+100;
    if(NH3_SI >= AQI)
    {
      AQI = NH3_SI;
      significantPollutant = "NH3";
    }
  }
  else if(NH3_val>=801.00 && NH3_val <= 1200.00)
  {
    double NH3_SI = ((300-200)/(1200-800)*(NH3_val-800))+200;
    if(NH3_SI >= AQI)
    {
      AQI = NH3_SI;
      significantPollutant = "NH3";
    }
  }
  else if(NH3_val>=1201.00 && NH3_val <= 1800.00)
  {
    double NH3_SI = ((400-300)/(1800-1200)*(NH3_val-1200))+300;
    if(NH3_SI >= AQI)
    {
      AQI = NH3_SI;
      significantPollutant = "NH3";
    }
  }
  else if(NH3_val>1800.00)
  {
    double NH3_SI = ((500-400)/(1801)*(NH3_val-1800))+400;
    if(NH3_SI >= AQI)
    {
      AQI = NH3_SI;
      significantPollutant = "NH3";
    }
  }




  GasSensorValue = analogRead(MQ9pin);  
  double CO_val = (GasSensorValue / GasFactor)*1.233*0.0212; 
 
  delay(1750);

  if(CO_val>=0.00 && CO_val <= 1.00)
  {
    double CO_SI = ((50-0)/(1-0)*(CO_val-0))+0;
    if(CO_SI >= AQI)
    {
      AQI = CO_SI;
      significantPollutant = "CO";
    }
  }
  else if(CO_val>=1.1 && CO_val <= 2.00)
  {
    double CO_SI = ((100-50)/(2-1)*(CO_val-1))+50;
    if(CO_SI >= AQI)
    {
      AQI = CO_SI; 
      significantPollutant = "CO";
    }
  }
  else if(CO_val>=2.1 && CO_val <= 10.00)
  {
    double CO_SI = ((200-100)/(10-2)*(CO_val-2))+100;
    if(CO_SI >= AQI)
    {
      AQI = CO_SI;
      significantPollutant = "CO"; 
    }
  }
  else if(CO_val>=10.1 && CO_val <= 17.00)
  {
    double CO_SI = ((300-200)/(17-10)*(CO_val-10))+200;
    if(CO_SI >= AQI)
    {
      AQI = CO_SI; 
      significantPollutant = "CO";
    }
  } 
  else if(CO_val>=17.1 && CO_val <= 34.00)
  {
    double CO_SI = ((400-300)/(34-17)*(CO_val-17))+300;
    if(CO_SI >= AQI)
    {
      AQI = CO_SI; 
      significantPollutant = "CO";
    }
  } 
  else if(CO_val>34.00)
  {
    double CO_SI = ((500-400)/(35)*(CO_val-34))+400;
    if(CO_SI >= AQI)
    {
      AQI = CO_SI; 
      significantPollutant = "CO";
    }
  }   
  



  float NO2_val = analogRead(A4)*0.04;  

  if(NO2_val>=0.00 && NO2_val <= 40.00)
  {
    double NO2_SI = ((50-0)/(40-0)*(NO2_val-0))+0;
    if(NO2_SI >= AQI)
    {
      AQI = NO2_SI;
      significantPollutant = "NO2";
    }
  }

  else if(NO2_val>=41.00 && NO2_val <= 80.00)
  {
    double NO2_SI = ((100-50)/(80-40)*(NO2_val-40))+50;
    if(NO2_SI >= AQI)
    {
      AQI = NO2_SI;
      significantPollutant = "NO2";
    }
  }
  
  else if(NO2_val>=81.00 && NO2_val <= 180.00)
  {
    double NO2_SI = ((200-100)/(180-80)*(NO2_val-80))+100;
    if(NO2_SI >= AQI)
    {
      AQI = NO2_SI;
      significantPollutant = "NO2";
    }
  } 
  else if(NO2_val>=181.00 && NO2_val <= 280.00)
  {
    double NO2_SI = ((300-200)/(280-180)*(NO2_val-180))+200;
    if(NO2_SI >= AQI)
    {
      AQI = NO2_SI;
      significantPollutant = "NO2";
    }
  }
  else if(NO2_val>=281.00 && NO2_val <= 400.00)
  {
    double NO2_SI = ((400-300)/(400-280)*(NO2_val-280))+300;
    if(NO2_SI >= AQI)
    {
      AQI = NO2_SI;
      significantPollutant = "NO2";
    }
  }
  else if(NO2_val>400.00)
  {
    double NO2_SI = ((500-400)/(401)*(NO2_val-400))+400;
    if(NO2_SI >= AQI)
    {
      AQI = NO2_SI;
      significantPollutant = "NO2";
    }
  }     





  digitalWrite(ledPower,LOW); 
  delayMicroseconds(samplingTime);
  voMeasured = analogRead(A0); 
  delayMicroseconds(deltaTime);
  digitalWrite(ledPower,HIGH); 
  delayMicroseconds(sleepTime);
  calcVoltage = voMeasured * (2.15 / 1024.0);
  dustDensity = 170 * calcVoltage - 0.1;
 
  double PM25_val = dustDensity*0.47; 

  if(PM25_val>=0.00 && PM25_val <= 30.00)
  {
    double PM25_SI = ((50-0)/(30-0)*(PM25_val-0))+0;
    if(PM25_SI >= AQI)
    {
      AQI = PM25_SI;
      significantPollutant = "PM2.5";
    }
  }
  else if(PM25_val>=31.00 && PM25_val <= 60.00)
  {
    double PM25_SI = ((100-50)/(60-30)*(PM25_val-30))+50;
    if(PM25_SI >= AQI)
    {
      AQI = PM25_SI;
      significantPollutant = "PM2.5";
    }
  }
  else if(PM25_val>=61.00 && PM25_val <= 90.00)
  {
    double PM25_SI = ((200-100)/(90-60)*(PM25_val-60))+100;
    if(PM25_SI >= AQI)
    {
      AQI = PM25_SI;
      significantPollutant = "PM2.5";
    }
  }
  else if(PM25_val>=91.00 && PM25_val <= 120.00)
  {
    double PM25_SI = ((300-200)/(120-90)*(PM25_val-90))+200;
    if(PM25_SI >= AQI)
    {
      AQI = PM25_SI;
      significantPollutant = "PM2.5";
    }
  }
  else if(PM25_val>=121.00 && PM25_val <= 250.00)
  {
    double PM25_SI = ((400-300)/(250-120)*(PM25_val-120))+300;
    if(PM25_SI >= AQI)
    {
      AQI = PM25_SI;
      significantPollutant = "PM2.5";
    }
  }
  else if(PM25_val>250.00)
  {
    double PM25_SI = ((500-400)/(251)*(PM25_val-250))+400;
    if(PM25_SI >= AQI)
    {
      AQI = PM25_SI;
      significantPollutant = "PM2.5";
    }
  }




  double PM10_val = dustDensity*0.59;

  if(PM10_val>=0.00 && PM10_val <= 50.00)
  {
    double PM10_SI = ((50-0)/(50-0)*(PM10_val-0))+0;
    if(PM10_SI >= AQI)
    {
      AQI = PM10_SI;
      significantPollutant = "PM10";
    }
  }
  else if(PM10_val>=51.00 && PM10_val <= 100.00)
  {
    double PM10_SI = ((100-50)/(100-50)*(PM10_val-50))+50;
    if(PM10_SI >= AQI)
    {
      AQI = PM10_SI;
      significantPollutant = "PM10";
    }
  }
  else if(PM10_val>=101.00 && PM10_val <= 250.00)
  {
    double PM10_SI = ((200-100)/(250-100)*(PM10_val-100))+100;
    if(PM10_SI >= AQI)
    {
      AQI = PM10_SI;
      significantPollutant = "PM10";
    }
  }
  else if(PM10_val>=251.00 && PM10_val <= 350.00)
  {
    double PM10_SI = ((300-200)/(350-250)*(PM10_val-250))+200;
    if(PM10_SI >= AQI)
    {
      AQI = PM10_SI;
      significantPollutant = "PM10";
    }
  } 
  else if(PM10_val>=351.00 && PM10_val <= 430.00)
  {
    double PM10_SI = ((400-300)/(430-350)*(PM10_val-350))+300;
    if(PM10_SI >= AQI)
    {
      AQI = PM10_SI;
      significantPollutant = "PM10";
    }
  }
  else if(PM10_val>430.00)
  {
    double PM10_SI = ((500-400)/(431)*(PM10_val-430))+400;
    if(PM10_SI >= AQI)
    {
      AQI = PM10_SI;
      significantPollutant = "PM10";
    }
  } 




  MQ131.sample();
  double O3_val = MQ131.getO3(UG_M3)*0.79*0.000000085; 

  if(O3_val>=0.00 && O3_val <= 50.00)
  {
    double O3_SI = ((50-0)/(50-0)*(O3_val-0))+0;
    if(O3_SI >= AQI)
    {
      AQI = O3_SI;
      significantPollutant = "O3";
    }
  }
  else if(O3_val>=51 && O3_val <= 100)
  {
    double O3_SI = ((100-50)/(100-50)*(O3_val-50))+50;
    if(O3_SI >= AQI)
    {
      AQI = O3_SI;
      significantPollutant = "O3";
    }
  }  
  else if(O3_val>=101 && O3_val <= 168)
  {
    double O3_SI = ((200-100)/(168-100)*(O3_val-100))+100;
    if(O3_SI >= AQI)
    {
      AQI = O3_SI;
      significantPollutant = "O3";
    }  
  }
  else if(O3_val>=169 && O3_val <= 208)
  {
    double O3_SI = ((300-200)/(208-168)*(O3_val-168))+200;
    if(O3_SI >= AQI)
    {
      AQI = O3_SI;
      significantPollutant = "O3";
    }  
  }
  else if(O3_val>=209 && O3_val <= 748)
  {
    double O3_SI = ((400-300)/(748-208)*(O3_val-208))+300; 
    if(O3_SI >= AQI)
    {
      AQI = O3_SI;
      significantPollutant = "O3";
    }  
  }
  else if(O3_val>748)
  {
    double O3_SI = ((500-400)/(749)*(O3_val-748))+400; 
    if(O3_SI >= AQI)
    {
      AQI = O3_SI;
      significantPollutant = "O3";
    }  
  }





  sensorValue = 0;
  for (int i = 0; i < extraBit; i++) 
  {
    sensorValue = analogRead(analogInPin) + sensorValue;
    delay(3);   
  }
  sensorValue = sensorValue - cOff; 
  //float SO2_val = (((float)sensorValue/extraBit/1024*Vref/resValue*1000000000)/Sf)*0.056; 
  float SO2_val = sensorValue*-0.00111681; 
  if(SO2_val < 0)
  {
    SO2_val = 1.57;
  }
  delay(218);
  
  if(SO2_val>=0.00 && SO2_val <= 40.00)
  {
    double SO2_SI = ((50-0)/(40-0)*(SO2_val-0))+0;
    if(SO2_SI >= AQI)
    {
      AQI = SO2_SI;
      significantPollutant = "SO2";
    }
  }
  else if(SO2_val>=41 && SO2_val <= 80)
  {
    double SO2_SI = ((100-50)/(80-40)*(SO2_val-40))+50;
    if(SO2_SI >= AQI)
    {
      AQI = SO2_SI;
      significantPollutant = "SO2";
    }
  }  
  else if(SO2_val>=81 && SO2_val <= 380)
  {
    double SO2_SI = ((200-100)/(380-80)*(SO2_val-80))+100;
    if(SO2_SI >= AQI)
    {
      AQI = SO2_SI;
      significantPollutant = "SO2";
    }  
  }
  else if(SO2_val>=381 && SO2_val <= 800)
  {
    double SO2_SI = ((300-200)/(800-380)*(SO2_val-380))+200;
    if(SO2_SI >= AQI)
    {
      AQI = SO2_SI;
      significantPollutant = "SO2";
    }  
  }
  else if(SO2_val>=801 && SO2_val <= 1600)
  {
    double SO2_SI = ((400-300)/(1600-800)*(SO2_val-800))+300; 
    if(SO2_SI >= AQI)
    {
      AQI = SO2_SI;
      significantPollutant = "SO2";
    }  
  }
  else if(SO2_val>1601)
  {
    double SO2_SI = ((500-400)/(1602)*(SO2_val-1600))+400; 
    if(SO2_SI >= AQI)
    {
      AQI = SO2_SI;
      significantPollutant = "SO2";
    }  
  }
 // send data to ESP32 via serial communication (UART Protocol)
                                  
  Serial.print(String((int)AQI)+"A"+String(O3_val)+"B"+String(SO2_val)+"C"+String(CO_val)+"D"+String(NH3_val)+"E"+String(NO2_val)+"F"+String(PM25_val)+"G"+String(PM10_val)+"H"+String((int)temperature)+"I"+String((int)humidity)+"J"+significantPollutant);                                   
  Serial.println();
}
