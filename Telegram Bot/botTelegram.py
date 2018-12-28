import requests
import json
import datetime
from bs4 import BeautifulSoup
from time import sleep
import sys

class Telegram():

	def __init__(self, token):
		self.token = token
		self.URL = URL = 'https://api.telegram.org/bot' + token + '/'
		self.last_update_id = 0
		self.last_time = 0
		self.last_message_id_is_one = True
		self.start = False
		self.interation = 0

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

	def getTimeAndDate(self):
	    dateURL = 'http://api.timezonedb.com/v2.1/list-time-zone'
	    key = 'key=LF343RPEO5MY'
	    typerequest = 'json'
	    country = 'RU'
	    zone = '*Kaliningrad*'
	    SendURL = dateURL + '?' + key + '&format=' + typerequest + '&country=' + country +'&zone=' + zone
	    r = requests.get(SendURL).json()
	    time = r['zones'][-1]['timestamp']
	    res = self.toTime(time)
	    return str(int(res[11:-6]) - 2) + res[13:] + ' ' + res[:-8]

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

		if self.last_message_id_is_one == False and self.start == True:

			current_update_id = self.getLastUpdate()['update_id']
			current_time = self.getSecInTime(self.toTime(self.getTimeMessage(self.getChatId())))
			options = ['/time - Current Moscow time', '/translate <text>']

			if current_update_id != self.last_update_id and current_time - self.last_time > 1 and current_time - self.last_time < 5:

				self.last_update_id = current_update_id
				self.last_time = current_time

				if message == '/help':
					for i in range(len(options)):
						self.sendMessage(self.getChatId(), options[i])
				elif message == '/time':
					self.sendMessage(self.getChatId(), self.getTimeAndDate())
				elif '/translate ' in message:
					self.sendMessage(self.getChatId(), self.translateYandex(message[11:]))
				elif message == '/start':
					self.sendMessage(self.getChatId(), 'I am already started!')
				else:
					self.sendMessage(self.getChatId(), 'I don\'t know what u want =/')	

		elif self.getChatId() != None:
			self.sendMessage(self.getChatId(), 'I was restarted!')
			self.start = True
			self.last_message_id_is_one = False

		else: 
			self.sendMessage(self.getChatId(), 'Welcome brother c:')
			current_time = self.getSecInTime(self.toTime(self.getTimeMessage(self.getChatId())))
			self.last_time = current_time - 3
			self.start = True
			self.last_message_id_is_one = False

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
		return res[2:-2]

	def jsonToFile(self, data):
		with open('data.json', 'w') as outfile:
			json.dump(data, outfile, sort_keys = True, indent = 4,
               ensure_ascii = False)

	def Online(self):
		while True:
			try:	
				self.function(self.getLastMessage())
				sleep(2)
			except IndexError:
				continue

def main():
	token = '**'
	bot = Telegram(token)
	bot.Online()
	
	#Проверка ответа от яндекс переводчика

if __name__ == '__main__':
	main()
