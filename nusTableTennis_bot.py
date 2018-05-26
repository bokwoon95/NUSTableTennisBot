import requests
import datetime
import RPi.GPIO as GPIO
import telepot as tele
import json

class BotHandler:
    # Initialize bot
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    # Get the latest replies from the user
    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, first_chat_id, text):
        params = {'first_chat_id': first_chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
           last_update = None
        return last_update

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


token = "500873036:AAFS4YzoMR6NSaUrjldYRukhx0FvkxUurDg" #Token of your bot
NUSTableTennisBot = BotHandler(token) #Your bot's name

machineState = False
invitationAccept = False

# def machineChecker():
    #print('User interacting with Machine')
    #message ='Do you want to play Table Tennis?'
    #keyboard = [[{"text":"Fast"}],[{"text":"Medium"}],[{"text:Slow"}]]
    #reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    #send_message(first_chat_id,message,json.dumps(reply_markup))

def speedController(first_chat_id,first_update_id):
    print('User setting Speed Control')
    message ='Set Machine Speed'
    #reply_markup = reply_markup_maker(['Fast'],['Medium'],['Slow'])
    keyboard = [[{"text":"Fast"}],[{"text":"Medium"}],[{"text:Slow"}]]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    send_message(first_chat_id,message,json.dumps(reply_markup))


def menu(first_chat_id,first_update_id):
    print('User in main menu')
    commands = ['play','set speed']
    reply_markup = NUSTableTennisBot.reply_markup_maker(commands)
    message = "What can I help you with today?"
    send_message(first_chat_id, message,reply_markup)

    sleep(0.5)

    while text.lower() not in commands:
        first_chat_id,text,first_update_id= get_last_id_text(get_updates(first_update_id+1))
        sleep(0.5)

    if text.lower()=='set speed':
        speedController(first_chat_id,first_update_id)

    elif text.lower()=='play':
        machineChecker(first_chat_id,first_update_id)

def main():
    global machineState
    global invitationAccept
    new_offset = 0
    print('Hi, NUSTableTennisBot now launching...')

    while True:
        all_updates=NUSTableTennisBot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text='New member'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"


                menu(first_chat_id, first_update_id)
                if first_chat_text == '/check':
                    if machineState == True:
                        NUSTableTennisBot.send_message(first_chat_id, 'There is a player playing. Do you want to join him/her? ' ) #+ first_chat_name)
                        new_offset = first_update_id + 1
                        if first_chat_text == '/yes' :
                            NUSTableTennisBot.send_message(first_chat_id, 'We will notify the players immediately, and get back to you soon.')
                            new_offset = first_update_id + 1
                        else:
                            NUSTableTennisBot.send_message(first_chat_id, 'Okay, I will see you soon.')
                            new_offset = first_update_id + 1
                    else:
                        NUSTableTennisBot.send_message(first_chat_id, 'There is currently no one playing with me. Do you want to come down and play with me?' ) #+ first_chat_name)
                        new_offset = first_update_id + 1
                elif first_chat_text == 'hi' :
                    NUSTableTennisBot.send_message(first_chat_id, 'Hi, how are you doing '+first_chat_name + '?')
                    new_offset = first_update_id + 1

# GPIO.setup(7, GPIO.IN)
# GPIO.setup(8, GPIO.IN)
# machineState = GPIO.input(7)
# invitationAccept = GPIO.input(8)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
         exit()
