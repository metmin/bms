#include <bq769x0.h>    // Library for Texas Instruments bq76920 battery management IC

// #define BMS_ALERT_PIN 2     // attached to interrupt INT0
// #define BMS_BOOT_PIN 7      // connected to TS1 input
#define BMS_I2C_ADDRESS 0x18

bq769x0 BMS(bq76930, BMS_I2C_ADDRESS);    // battery management system object

float voltage[10]={0,0,0,0,0,0,0,0,0,0};
int temp=0;
int batVolt=0;
String data=""; 
char v='0';
int k=0;
void setup()
{
  pinMode(PA2, OUTPUT);
  pinMode(PA5, INPUT);


Serial.begin(9600);
  int err = BMS.begin(PA5, PA2);

  BMS.setTemperatureLimits(-20, 45, 0, 45);
  BMS.setShuntResistorValue(5);
  BMS.setShortCircuitProtection(20000, 400);  // delay in us
  BMS.setOvercurrentChargeProtection(15000, 320);  // delay in ms
  BMS.setOvercurrentDischargeProtection(15000, 320); // delay in ms
  BMS.setCellUndervoltageProtection(3000, 8); // delay in s
  BMS.setCellOvervoltageProtection(4200, 2);  // delay in s

  BMS.setBalancingThresholds(0, 3300, 20);  // minIdleTime_min, minCellV_mV, maxVoltageDiff_mV
  BMS.setIdleCurrentThreshold(100);
  BMS.enableAutoBalancing();
  BMS.enableDischarging();
  BMS.getBatteryVoltage(); // mV
 pinMode(PC13, OUTPUT);
  digitalWrite(PC13, LOW);
      // turn the LED on (HIGH is the voltage level)
               // wait for a second


 
}

void loop()
{
   for(k;k<=3;k++)
 {

   digitalWrite(PC13, LOW);
   delay(300);
   digitalWrite(PC13,HIGH);
   delay(300);  
 
 }

  BMS.update();
  
  data = "";
  batVolt=BMS.getBatteryVoltage();
  temp=BMS.getTemperatureDegC();
   for(int i=0;i<10;i++)
 {
  voltage[i]=BMS.getCellVoltage(i+1);
  data += "voltage";
  data += i;
  data += "="; 
  data += voltage[i];
  data += ",";
 }

  data += "batvolt=";
  data += batVolt;
  data += ",temp=";
  data += temp;
  v=Serial.read();
 if(v=='a')
 {
    Serial.print(data);
  }
       
  delay(250);
  
  
}