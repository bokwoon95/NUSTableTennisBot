import requests
import json
import telegram

token = "577090085:AAFVzW4Z3dG7W0vcL3jdrW7pYFIGwvHrNCc" #Token of your bot
url = 'https://api.telegram.org/bot{}/'.format(token)
machineState = True
isSomeonePlaying = True

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

def sendGreenLightMessageToArduino():
    return True
        
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
    try:
        while True:
            main()
    except KeyboardInterrupt:
         exit()
