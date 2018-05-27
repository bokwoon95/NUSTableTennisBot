// Global Variables
// Handshake
int ACK= 0, NACK = 1, HELLO = 2;
// Machine State
int MACHINE_IS_ON = 3, MACHINE_IS_OFF = 4;
// Speed
int SLOW = 5, MEDIUM = 6, FAST = 7;
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
void changeSpeed(){
  int reply;
  if (Serial.available()) {
      reply = Serial.read();
      reply = reply - 48;
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

// Method to find out the previous values

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  handshake();
}

void loop() {
  // put your main code here, to run repeatedly:
}

