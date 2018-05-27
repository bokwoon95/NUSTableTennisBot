import requests
import datetime
import json
#import serial
import time

#ser = serial.Serial("dev/dev/ttyACM0",9600,timeout=1)
#ACK = b"\x00"
#NACK = b"\x01"
#HELLO = b"\x02"

machineState = True#Machine is ON

#while machineState:
#	time.sleep(1)
#	ser.write(Hello)
#	str = ser.read()
#	reply = int.from_bytes(str,byteorder = 'big', signed = True)
#	if(reply = 0):
#		machineState = False
#		ser.write(ACK)
#		print("Handshake completed")


invitation = False #There is no invitation

class BotHandler:
	def __init__(self, token):
		self.token = token
		self.api_url = "https://api.telegram.org/bot{}/".format(token)

#url = "https://api.telegram.org/bot<token>/"

	def get_updates(self, offset=None, timeout=30):
		method = 'getUpdates'
		params = {'timeout': timeout, 'offset': offset}
		resp = requests.get(self.api_url + method, params)
		result_json = resp.json()['result']
		return result_json

	def send_message(self, chat_id, text, reply_markup=None):
		params = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup, 'parse_mode': 'HTML'}
		method = 'sendMessage'
		if reply_markup:
			method = 'sendMessage' + '&reply_markup={}' 
		resp = requests.post(self.api_url + method, params)
		#TTTBot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		return resp
	
	def get_first_update(self):
		get_result = self.get_updates()

		if len(get_result) > 0:
			last_update = get_result[0]
		else:
			last_update = None

		return last_update

#	def reply_markup(self,data):
#		keyboard = []
#		for i in range(0,len(data),2):
#			key = []
#			key.append(data[i].title())
#			try:
#				key.append(data[i+1].title())
#			except:
#				pass
			
#			keyboard.append(key)
			   
#		reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
#		return json.dumps(reply_markup)

# takes in entire history of updates & returns only the latest one
def get_last_update_id(updates):
	print("YOYOYOYO SUCK A DICK")
	print(updates)
	update_ids = []
	for update in updates:
		update_ids.append(int(update["update_id"]))
	print(update_ids)
	return max(update_ids)


token = "455583182:AAEmTvauJXJ20d21wJOjMmwHgU1tccAj0As"
TTTBot = BotHandler(token) #Your bot's name

def machineChecking(first_chat_id, first_chat_text, first_update_id, new_offset):
	print("User at machine checking")

	if machineState == True:
		
		TTTBot.send_message(first_chat_id,'There is one player, do you want to challenge?')
#		commands = ['Yes','No']
#		reply_markup = TTTBot.reply_markup(commands)
		print ('test')
#		TTTBot.send_message(first_chat_id,'OK!',reply_markup)
		#first_chat_text = TTTBot.get_first_update()['message']['text']
		first_chat_text = get_last_update_id(TTTBot.get_updates())['message']['text']
		print (first_chat_text)
		
		x = True
		while x == True:
			if first_chat_text == 'yes':
				TTTBot.send_message(first_chat_id, 'I will inform the person right now')
				invitation = True
				x == False
				new_offset = first_update_id + 1
			elif first_chat_text == 'no':
				TTTBot.send_message(first_chat_id, 'I will see you next time then.')
				invitation = False
				x == False
				exit()

	else:
		TTTBot.send_message(first_chat_id, 'There is no player at the moment. You should come and play with me.')
		exit()

def main():
	new_offset = 0
	print('Now launching...')

	while True:
		all_updates=TTTBot.get_updates(new_offset)

		if len(all_updates) > 0:
			for current_update in all_updates:
				print(current_update)
				first_update_id = current_update['update_id']
				if 'text' not in current_update['message']:
					first_chat_text='New member'
					print(first_chat_text)
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

				if first_chat_text == 'Hi':
					TTTBot.send_message(first_chat_id, 'Morning ' + first_chat_name)
					machineChecking(first_chat_id,first_chat_text, first_update_id, new_offset)
				else:
					TTTBot.send_message(first_chat_id, 'How are you doing '+first_chat_name)
					new_offset = first_update_id + 1


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()

