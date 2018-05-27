/*set up LCD RGB*/
#include <Wire.h>
#include "rgb_lcd.h"

void Solo();
rgb_lcd lcd;

const int colorR = 50;
const int colorG = 255;
const int colorB = 100;

/*-------definning Outputs------*/
#define LM1 12       // left motor
#define LM2 13       // left motor
#define RM1 7      // right motor
#define RM2 4      // right motor
#define L_motoren 11  //left motor enable
#define R_motoren 6  //right motor enable
#define button 9
#define Touch 3
#define LED 8

int PowerOn = 1;
int buttonState = 0;
int touchState = 0;
int angle = 0;  
int rotdir=0; 
int velocity;
int Chanllenger = 0;
int dis=0;

// Global Variables
// Handshake
int16_t ACK= 0, NACK = 1, HELLO = 2;
// Machine State
int16_t MACHINE_IS_ON = 3, MACHINE_IS_OFF = 4;
// Speed
int16_t SLOW = 5, MEDIUM = 6, FAST = 7;
int SLOW_SPEED, MEDIUM_SPEED, FAST_SPEED;

// Change States
int previousPotientialMeterValue = 0;
int potientialMeterValue = 0;
int softwareSpeed = 0;
int isSoftwareControl = true;

// Method to Check if Machine changes state
// Data Sent: Tell the RasberryPi if the Machine is turned on or off
void checkMachineState(){
  if(potientialMeterValue > 0 && previousPotientialMeterValue == 0){
    Serial.print(MACHINE_IS_ON);
  } else if (potientialMeterValue == 0 && previousPotientialMeterValue > 0){
    Serial.print(MACHINE_IS_OFF);
  }
}

// Method to change Speed
// Not Used
void changeSpeed(){
  int reply;
  if (Serial.available()) {
      reply = Serial.read();
      reply = reply-48;
      if(reply == SLOW){
        softwareSpeed = SLOW_SPEED;
      } else if(reply == MEDIUM){
        softwareSpeed = MEDIUM_SPEED;
      } else if(reply == FAST){
        softwareSpeed = FAST_SPEED;
      }
      isSoftwareControl = true;
  } else if (potientialMeterValue != previousPotientialMeterValue){
    isSoftwareControl = false;
  }
}

// Method to Handshake with the RaspberryPI
void handshake() {
  int reply;
  int handshake_flag = 1;
  
  while (handshake_flag == 1) {
    if (Serial.available()) {
      reply = Serial.read();
      reply = reply - 48;
      if (reply == HELLO) {
        Serial.print(ACK);
      }
      if (reply == ACK) {
        handshake_flag = 0;
      }
    }
  }
}

void checkGreenLight(){
  if (Serial.available()) {
    reply = Serial.read();
    reply = reply - 48;
    if (reply == 8) {
      Challenger = 1;
    }
  }
}

// Method to find out the previous values

void setup() {
  // put your setup code here, to run once:
  pinMode(LM1, OUTPUT);
  pinMode(LM2, OUTPUT);
  pinMode(RM1, OUTPUT);
  pinMode(RM2, OUTPUT);
  pinMode(L_motoren, OUTPUT);
  pinMode(R_motoren, OUTPUT);
  pinMode(button,INPUT_PULLUP);
  pinMode(Touch,INPUT_PULLUP);
  //  servo_test.attach(3);      // attach the signal pin of servo to pin3 of arduino
  // set up the LCD's number of columns and rows:

  Serial.begin(115200);
  handshake();
  
  lcd.begin(16, 2);
  
  lcd.setRGB(colorR, colorG, colorB);
  
  // Print a message to the LCD.
  lcd.print("Solo Mode");
}

void loop() {
  // put your main code here, to run repeatedly:
  int potValue = analogRead(A0); // Read potentiometer value
  int pwmOutputL = map(potValue, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  int pwmOutputR = map(potValue, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  //velocity = map(potValue, 0, 1023, 0, 10);//map speed
  potientialMeterValue = potValue;
  checkMachineState();
  
  analogWrite (L_motoren, pwmOutputL);
  analogWrite (R_motoren, pwmOutputR);
  //debounce button
  buttonState=digitalRead(button);
  delay(20);
  if(buttonState){
    if(PowerOn){
      PowerOn=0;
    }else{
      PowerOn=1;
    }
  }
  //debounce touch
  touchState=!digitalRead(Touch);
  delay(20);
  if(touchState==0){
    Chanllenger=!Chanllenger;
  }

  if(Chanllenger==0){
    digitalWrite(LED,LOW);
    if(dis==0){
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Solo Mode");
    dis=1;
    }
    if(PowerOn){
    digitalWrite(LM2, LOW);
    digitalWrite(LM1, HIGH);
    digitalWrite(RM2, LOW);
    digitalWrite(RM1, HIGH);
    }
    if(PowerOn==0){
    digitalWrite(LM1, LOW);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, LOW);
    digitalWrite(RM2, LOW);
    }
  }
  if(Chanllenger){
    dis=0;
    digitalWrite(LM1, LOW);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, LOW);
    digitalWrite(RM2, LOW);
    digitalWrite(LED,HIGH);
    lcd.setCursor(0,0);
    lcd.print("Chanllenger!!!");
  }
  previousPotientialMeterValue = potientialMeterValue;
}

