
#include <Arduino.h>
#include <SoftwareSerial.h>
#include <stdio.h>
#include <stdlib.h>

// Packet code
int16_t ACK = 0, NAK = 1, HELLO = 2, READ = 3, WRITE = 4, DATA_RESP = 5;

// Method to Handshake with the RaspberryPI
void handshake() {
  int reply;
  int handshake_flag = 1;
  
  while (handshake_flag == 1) {
    if (Serial.available()) {
      reply = Serial.read();
      if (reply == HELLO) {
        Serial.write(ACK);
      }
      if (reply == ACK) {
        handshake_flag = 0;
      }
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  handshake();
}

void loop() {
  // put your main code here, to run repeatedly:
}
