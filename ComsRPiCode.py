import serial
import time
ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

# Declare Global Variables
# Hand Shake
ACK = b"\x00"
NACK = b"\x01"
HELLO = b"\x02"
# Machine State
MACHINE_IS_ON = b"\x03"
MACHINE_IS_OFF = b"\x04"
machineState = False
# Speed
SLOW = b"\x05"
MEDIUM = b"\x06"
FAST = b"\x07"

# Handshake Beteen Rasberry Pi and Arduino
# Return: None
def handshake(handshake_flag):
    while handshake_flag:
        time.sleep(1)
        ser.write(HELLO)
        string = ser.read()
        reply = int.from_bytes(string, byteorder='big', signed=True)
        if (reply == ACK):
            handshake_flag = False
            ser.write(ACK)
            print('Handshake completed')

# Funcion to Check the Machine State
# Data Received: Machine State if data is recieved from the Arduino 
# Return: machineState (Boolean)
def checkMachineState():
    while ser.in_waiting:
        string = ser.red()
        reply = int.from_bytes(string, byteorder="big", signed=True)
        if (reply == MACHINE_IS_OFF):
            machineState = False
        elif(reply == MACHINE_IS_ON):
            machineState = True
        
    return machineState

# Function to Change Speed
# Data Send: Send User's speed requested to the Arduino
# Return: Booleam
def changeSpeed(text):
    if text.lower == "slow":
        ser.write(SLOW)
        return True
    elif text.lower == "medium":
        ser.write(MEDIUM)
        return True
    elif text.lower == "fast":
        ser.write(FAST)
        return True
    return False
            
handshake(True)

