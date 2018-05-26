// Packet code
int ACK= 0;
int HELLO = 2;


// Method to Handshake with the RaspberryPI
void handshake() {
  int reply;
  int handshake_flag = 1;
  
  while (handshake_flag == 1) {
    if (Serial.available()) {
      reply = Serial.read();
      reply = reply - 48;
      Serial.print( reply == HELLO);
      if (reply == HELLO) {
        Serial.print(ACK);
      }
      if (reply == ACK) {
        handshake_flag = 0;
      }
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  handshake();
}

void loop() {
  // put your main code here, to run repeatedly:
}
