import requests
import json
from time import sleep
from telegram.ext.dispatcher import run_async

token = "577090085:AAFVzW4Z3dG7W0vcL3jdrW7pYFIGwvHrNCc" #Token of your bot
url = 'https://api.telegram.org/bot{}/'.format(token)
machineState = True

# Get Own User
# Currently Used
def getme():
    res=requests.get(url+"getme")
    data = res.json()
    username = data['result']['username']

# Updates the New User
def get_updates(offset = None):
    try:
        URL = url + 'getUpdates'
        if offset:
            URL += '?offset={}'.format(offset)

        res = requests.get(URL)
        while (res.status_code !=200 or len(res.json()['result'])== 0):
            sleep(1)
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
    try:
        text = last_update['message']['text']
    except:
        text = ''
    return chat_id,text,update_id

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
        chat_id,text,update_id = get_last_id_text(get_updates())
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

def end(chat_id,text,update_id):
    message = 'Do you wanna end?'
    reply_markup = reply_markup_maker(['Yes','No'])
    send_message(chat_id,message,reply_markup)
    chat_id,text,update_id = get_last_id_text(get_updates())

    if text.lower() =='yes':
        return 'y'
    elif text.lower() == 'no':
        return 'n'
    else:
        spawnNewUser(update_id)

# Menu
# Called: When a user starts the bot
# Returns: none
def menu(chat_id,text,update_id):
    print('User in main menu')
    message = 'Select'
    commands = ['Machine Checker','Speed Controller']
    reply_markup = reply_markup_maker(commands)
    send_message(chat_id,message,reply_markup)
    chat_id,text,update_id = get_last_id_text(get_updates())

    if text.lower() == 'machine checker':
        machineChecker(chat_id, update_id)
    elif text.lower() == 'speed controller':
        print('User should be at speed controller')
        message = 'you are controlling your speed now'
    else:
        spawnNewUser(update_id)
    return

# Starts Bot
# Called: When the bot starts
def start(chat_id):
    print('Users at start')
    message = 'Wanna Start?'
    reply_markup=reply_markup_maker(['Start'])
    send_message(chat_id,message,reply_markup)
    chat_id,text,update_id = get_last_id_text(get_updates())
    
    if text.lower() == 'start':
        return 'n'
    else:
        spawnNewUser(update_id)
    return

# Create New User
# Called: Whenever a new user joins
# Returns: none
def spawnNewUser(update_id):
    chat_id,text,update_id = get_last_id_text(get_updates(update_id+1))
    menu(chat_id,text,update_id)
    sleep(0.5)    

# Main Function
# Called: When user starts the bot
# Return: None
def main():
    chat_id, text, update_id = get_last_id_text(get_updates())
    text = start(chat_id)
    while text.lower() !='y':
        menu(chat_id,text,update_id)
        text = end(chat_id,text,update_id)
    

# Start
if __name__ == '__main__':
    print('Hi, NUSTableTennisBot now launching...')
    try:
        main()
    except KeyboardInterrupt:
         exit()