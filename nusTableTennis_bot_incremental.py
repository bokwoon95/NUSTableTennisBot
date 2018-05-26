import requests
import json
from time import sleep

token = "500873036:AAFS4YzoMR6NSaUrjldYRukhx0FvkxUurDg" #Token of your bot
url = 'https://api.telegram.org/bot{}/'.format(token)
machineState = False

def getme():
    res=requests.get(url+"getme")
    d = res.json()
    username = d['result']['username']

def get_updates(offset = None):
    while True:
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

def get_last(data):

    results = data['result']
    count = len(results)
    last = count -1
    last_update = results[last]
    return last_update


def send_message(chat_id, text,reply_markup=None):
    URL = url+"sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text,chat_id)
    if reply_markup:
        URL += '&reply_markup={}'.format(reply_markup)
    res = requests.get(URL)
    while res.status_code != 200:
        res= requests.get(URL)
#    print(res.status_code)


def get_last_id_text(updates):
    last_update = get_last(updates)
    chat_id =last_update['message']['chat']['id']
    update_id = last_update['update_id']
    try:
        text = last_update['message']['text']
    except:
        text = ''
    return chat_id,text,update_id

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

def machineChecker(chat_id,machineState, update_id):
    print('User in Machine Checker')
    if machineState == True:
        message = "There is a player, do you want to challange?" #GPIO.input()
        commands = ['Yes', 'No']
        reply_markup = reply_markup_maker(commands)
        send_message(chat_id,message,reply_markup)
        chat_id, text, update_id = get_last_id_text(get_updates(update_id+1))
    else:
        message = "There is no player as of now. You should come and train with me."
        chat_id, text, update_id = get_last_id_text(get_updates(update_id+1))

    return chat_id, text, update_id

def menu(chat_id,text,update_id):
    print('User in main menu')
    message = 'Select'
    commands = ['Machine Checker','Speed Controller']
    reply_markup = reply_markup_maker(commands)
    send_message(chat_id,message,reply_markup)
    print(text)
    chat_id,text,update_id = get_last_id_text(get_updates())

    while text.lower() not in commands:
        chat_id,text,update_id = get_last_id_text(get_updates(update_id+1))
        sleep(0.5)

    if text.lower() == 'machine checker':
        machineChecker(chat_id, machineState, update_id)
        sleep(0.5)
    elif text.lower() == 'speed controller':
        print('User should be at speed controller')
        message = 'you are controlling your speed now'

def start(chat_id):
    print('Users at start')
    message = 'Wanna Start'
    reply_markup=reply_markup_maker(['Start'])
    send_message(chat_id,message,reply_markup)

    chat_id,text,update_id = get_last_id_text(get_updates())
    while(text.lower() != 'start'):
        chat_id,text,update_id= get_last_id_text(get_updates(update_id+1))
        sleep(0.5)

    return chat_id,text,update_id


def end(chat_id,text,update_id):
    message = 'Do you wanna end?'
    reply_markup = reply_markup_maker(['Yes','No'])
    send_message(chat_id,message,reply_markup)

    new_text =text
    while(text == new_text):
        chat_id,new_text,update_id= get_last_id_text(get_updates(update_id+1))
        sleep(1)
    if new_text =='Yes':
        return 'y'
    else:
        return 'n'


def main():
    print('Hi, NUSTableTennisBot now launching...')
    text = ' '
    chat_id, text, update_id = get_last_id_text(get_updates())
    chat_id,text,update_id = start(chat_id)
    while text.lower() != 'y':
        sleep(1)
        text = 'start'
        menu(chat_id,text,update_id)
        print(text ,'at main')
        text = 'y'

        chat_id, text, update_id = get_last_id_text(get_updates())
        text = end(chat_id,text,update_id)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
         exit()
