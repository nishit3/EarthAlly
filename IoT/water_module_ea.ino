#include <SimpleTimer.h>
#include "GravityTDS.h"

#define TdsSensorPin A2
GravityTDS gravityTds;
 
float tdsValue = 0;

SimpleTimer timer;
float calibration_value = 21.34 - 0.7;
int phval = 0; 
unsigned long int avgval; 
int buffer_arr[10],temp;
float ph_act;

int turbiditySensorPin = A1;
float turbidityVolt;
float ntu;

void setup() {
  Serial.begin(9600);
  pinMode(A0, OUTPUT);
  gravityTds.setPin(TdsSensorPin);
  gravityTds.setAref(5.0);  
  gravityTds.setAdcRange(1024);
  gravityTds.begin();  
}

void loop() {

  // pH
  timer.run(); 
  for(int i=0;i<10;i++) 
  { 
    buffer_arr[i]=analogRead(A0);
    delay(30);
  }
  for(int i=0;i<9;i++)
  {
    for(int j=i+1;j<10;j++)
    {
      if(buffer_arr[i]>buffer_arr[j])
      {
        temp=buffer_arr[i];
        buffer_arr[i]=buffer_arr[j];
        buffer_arr[j]=temp;
      }
    }
  }
  avgval=0;
  for(int i=2;i<8;i++)
  avgval+=buffer_arr[i];
  float volt=(float)avgval*5.0/1024/6; 
  ph_act = (-5.70 * volt + calibration_value)*0.564;


  // turbidity
  turbidityVolt = 0;
  for(int i=0; i<800; i++)
  {
    turbidityVolt += ((float)analogRead(turbiditySensorPin)/1023)*5;
  }
  turbidityVolt = turbidityVolt/800;
  if(turbidityVolt < 2.5){
    ntu = 3000;
  }else{
    ntu = (-1120.4*square(turbidityVolt)+5742.3*turbidityVolt-4353.8)*0.363*0.0035; 
  }


  // TDS
  gravityTds.setTemperature(27);  // set the temperature and execute temperature compensation
  gravityTds.update();  //sample and calculate
  tdsValue = (gravityTds.getTdsValue())*900;

  // Send data to ESP32 via serial communication
  Serial.print(String(ph_act)+"A"+String(ntu)+"B"+String(tdsValue));
  Serial.println();
  delay(4000);
}
