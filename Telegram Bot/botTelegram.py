import requests
import json
import datetime
from bs4 import BeautifulSoup
from time import sleep
import re
import sys, os
sys.path.append(os.path.abspath(__file__))
from misc import token

class Telegram():

	def __init__(self, token):

		self.token = token
		self.URL = URL = 'https://api.telegram.org/bot' + token + '/'
		self.last_update_id = 0
		self.last_time = 0
		self.start = False

	def getMe(self):
		localURL = self.URL + 'getMe'
		r = requests.get(localURL)
		return r.json()

	def getUpdates(self):
		localURL = self.URL + 'getupdates'
		r = requests.get(localURL)
		return r.json()

	def getLastUpdate(self):

		return self.getUpdates()['result'][-1]

	def getLastMessage(self):

		return self.getLastUpdate()['message']['text']

	def getChatId(self):

		return str(self.getLastUpdate()['message']['chat']['id'])

	def getLastMessageId(self):

		return int(self.getLastUpdate()['message']['message_id'])

	def getSecInTime(self, timestr):

		return int(timestr[17:])

	def getTimeMessage(self, chat_id):

		return int(self.getLastUpdate()['message']['date'])

	def toTime(self, timest):

		return datetime.datetime.fromtimestamp(timest).strftime('%Y-%m-%d %H:%M:%S')

	def sendMessage(self, chat_id, text):
		try:
			localURL = self.URL + 'sendMessage?chat_id='+ str(chat_id) + '&text=' + str(text)
			requests.get(localURL)
		except Exception as e:
			file = open('errors.txt', 'a')
			file.write('\n1. ' + str(e))

	def function(self, message):

		current_update_id = self.getLastUpdate()['update_id']
		current_time = self.getSecInTime(self.toTime(self.getTimeMessage(self.getChatId())))

		if current_update_id != self.last_update_id and current_time - self.last_time > 1:

			self.last_update_id = current_update_id
			self.last_time = current_time

			if message == '/help':
				self.sendMessage(self.getChatId(), 'use /translate < what to translate > and all will translated on Russian language!')

			elif message == '/start':
				self.sendMessage(self.getChatId(), 'Hi ! Read /help and goodluck!')

			elif '/translate' in message:
					self.sendMessage(self.getChatId(), self.translateYandex(message[11:]))

			elif message == '/restartbot':
				self.sendMessage(self.getChatId(), 'W8 I start restarted!')
				os.system("python3 restart.py restart")
				os.exit(0)
			else:

				self.sendMessage(self.getChatId(), 'I don\'t know what u want =/')	

	def checkMessage(self, message):

		if message == '':
			message = 'Your message was blank...'
			return str(message)
		else: return str(message)

	def translateYandex(self, message):

		localURL = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
		key = 'key=trnsl.1.1.20181225T000211Z.514e88abcce89674.b567950984e5b4104cbc6a5e4637314d3f44e28d&'
		lang = 'lang=ru&'
		formatAns = 'format=plain'

		SendURL = localURL + key + 'text=' + self.checkMessage(message) + '&' + lang + formatAns
		res = requests.get(SendURL).json()
		res = str(res['text'])

		if self.checkAnswerTranslate(res[2:-2]):
			return res[2:-2]
		else:
			return 'Enter more correctly or otherwise..'

	def jsonToFile(self, data):
		with open('data.json', 'w') as outfile:
			json.dump(data, outfile, sort_keys = True, indent = 4,
               ensure_ascii = False)

	def checkletterAnswer(self, letter):

		return bool(re.search('[а-яА-Я?!.\-:\s]', letter))

	def checkAnswerTranslate(self, text):
		count = 0
		for i in text:
			if self.checkletterAnswer(i) == True:
				count+=1
		if count == len(text):
			return True
		else: 
			return False

	def Online(self):

		self.sendMessage(self.getChatId(), 'Bot was restarted!')

		lastMessageId = self.getLastMessageId()

		while True:
			try:
				if lastMessageId < self.getLastMessageId():
					self.function(self.getLastMessage())
					sleep(2)
			except IndexError:
				continue

def main():
	bot = Telegram(token)
	bot.Online()

if __name__ == '__main__':
	main()
