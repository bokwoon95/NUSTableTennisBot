import requests
import json
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
GREEN_LIGHT = b"\x08"

token = "577090085:AAFVzW4Z3dG7W0vcL3jdrW7pYFIGwvHrNCc" #Token of your bot
url = 'https://api.telegram.org/bot{}/'.format(token)
machineState = True
isSomeonePlaying = True

# Handshake Beteen Rasberry Pi and Arduino
# Return: None
def handshake(handshake_flag):
    while handshake_flag:
        time.sleep(1)
        ser.write(HELLO)
        string = ser.read()
        reply = int.from_bytes(string, byteorder='big', signed=True)
        if (reply == 0):
            handshake_flag = False
            ser.write(ACK)
            print('Handshake completed')

# Funcion to Check the Machine State
# Data Received: Machine State if data is recieved from the Arduino
# Return: machineState (Boolean)
def checkMachineState():
    while ser.in_waiting:
        string = ser.read()
        reply = int.from_bytes(string, byteorder="big", signed=True)
        if (reply == MACHINE_IS_OFF):
            machineState = False
        elif(reply == MACHINE_IS_ON):
            machineState = True

    return machineState

# Function to Change Speed
# Data Send: Send User's speed requested to the Arduino
# Return: Boolean
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

# Function to Change Speed
# Data Send: Send User's speed requested to the Arduino
# Return: Boolean
def sendGreenLightMessageToArduino():
    ser.write(GREEN_LIGHT)
    return True

# Get Own User
# Currently Used
def getme():
    res=requests.get(url+"getme")
    data = res.json()
    username = data['result']['username']
    return username;

# Updates the New User
def get_updates(offset = None):
    try:
        URL = url + 'getUpdates'
        if offset:
            URL += '?offset={}'.format(offset)

        res = requests.get(URL)
        while (res.status_code !=200 or len(res.json()['result'])== 0):
            res = requests.get(URL)
        print(res.url)
        return res.json()
    except:
        pass;

# Get the Last Updated Data
def get_last(data):
    results = data['result']
    count = len(results)
    last = count -1
    last_update = results[last]
    return last_update

# Get the last text id
def get_last_id_text(updates):
    last_update = get_last(updates)
    chat_id =last_update['message']['chat']['id']
    update_id = last_update['update_id']
    first_name = last_update['message']['from']['first_name']
    try:
        text = last_update['message']['text']
    except:
        text = ''
    return chat_id,text,update_id,first_name

# Send a message to the user
def send_message(chat_id, text,reply_markup=None):
    URL = url+"sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text,chat_id)
    if reply_markup:
        URL += '&reply_markup={}'.format(reply_markup)
    res = requests.get(URL)
    while res.status_code != 200:
        res= requests.get(URL)

# Create Markup Maker
def reply_markup_maker(data):
    keyboard = []
    for i in range(0,len(data),2):
        key =[]
        key.append(data[i].title())
        try:
            key.append(data[i+1].title())
        except:
            pass
        keyboard.append(key)
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

# Checks to see if there is a player nearby
def machineChecker(chat_id, update_id):
    print('User in Machine Checker')
    if machineState:
        message = "There is a player, do you want to challange?" #GPIO.input()
        commands = ['Yes', 'No']
        reply_markup = reply_markup_maker(commands)
        send_message(chat_id,message,reply_markup)
        chat_id,text,update_id,first_name = get_last_id_text(get_updates(update_id+1))
        if text.lower() == 'yes':
            message = "Prepare to rumble"
            send_message(chat_id,message)
        elif text.lower() == 'no':
            message = "No worriess, I will give you a challenge"
            send_message(chat_id,message)
        else:
            spawnNewUser(update_id)
    else:
        message = "There is no player as of now. Come and train with me!"
        send_message(chat_id,message)
    return

# Checks to see if there is a player nearby
def playByYourself(chat_id, text, update_id):
    return chat_id, text, update_id

def end(chat_id,text,update_id,first_name):
    message = 'Do you wanna end?'
    reply_markup = reply_markup_maker(['Yes','No'])
    send_message(chat_id,message,reply_markup)
    chat_id,text,update_id,first_name = get_last_id_text(get_updates(update_id+1))
    if text.lower() == 'yes':
        text = "end"
        return chat_id,text,update_id,first_name
    elif text.lower() == 'no':
        return chat_id,text,update_id,first_name

# Send Green Light to Arduino
# Called: When the bot starts
def sendGreenLight(chat_id, text, update_id,first_name):
    print('Sending Green Light')
    sendGreenLightMessageToArduino()
    message = 'Playing user has been informed that you are coming!'
    send_message(chat_id,message)
    chat_id, text, update_id,first_name = get_last_id_text(get_updates())
    return chat_id, text, update_id,first_name

# Ask to user o join session
# Called: main()
# Returns: Boolean
def askToJoinSession(chat_id,text,update_id,first_name):
    print('Ask User if they want to join')
    message = 'Hi a user is playing, do you want to join?'
    commands = ['Yes','No']
    reply_markup = reply_markup_maker(commands)
    send_message(chat_id,message,reply_markup)
    chat_id,text,update_id,first_name = get_last_id_text(get_updates(update_id+1))
    return chat_id,text,update_id,first_name

# Starts Bot
# Called: When the bot starts
def start(chat_id,text,update_id,first_name):
    print('Users at start')
    message = 'Hi '+ first_name +' wanna start?'
    reply_markup = reply_markup_maker(['Start'])
    send_message(chat_id,message,reply_markup)
    chat_id,text,update_id,first_name = get_last_id_text(get_updates(update_id+1))

    if text.lower() == 'start':
        return chat_id,text,update_id,first_name

# Main Function
# Called: When user starts the bot
# Return: None
def main():
    chat_id,text,update_id,first_name = get_last_id_text(get_updates())
    # Until the User Presses Start
    chat_id,text,update_id,first_name = start(chat_id,text,update_id,first_name)
    while text.lower() != 'start':
        chat_id,text,update_id,first_name = start(chat_id,text,update_id,first_name)

    while text.lower() != 'end':
        while isSomeonePlaying != True:
           chat_id, text, update_id,first_name = playByYourself(chat_id, text, update_id,first_name)

        chat_id, text, update_id,first_name = askToJoinSession(chat_id, text, update_id,first_name)

        if text.lower() == 'yes':
            chat_id, text, update_id,first_name = sendGreenLight(chat_id, text, update_id,first_name)

        chat_id,text,update_id,first_name = end(chat_id,text,update_id,first_name)

    message = 'Thank you for using Awesome Table Tennis Bot'
    send_message(chat_id,message)

# Start
if __name__ == '__main__':
    print('Hi, NUSTableTennisBot now launching...')
    # handshake(True)
    try:
        while True:
            main()
    except KeyboardInterrupt:
         exit()
