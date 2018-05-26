import requests
import json
from time import sleep

token = "500873036:AAFS4YzoMR6NSaUrjldYRukhx0FvkxUurDg" #Token of your bot
url = 'https://api.telegram.org/bot{}/'.format(token)
machineState = False

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
