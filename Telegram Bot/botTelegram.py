# -*- coding: utf-8 -*-

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
        self.chat_id_list = []

    def getMe(self):
        localURL = self.URL + 'getMe'
        r = requests.get(localURL)
        return r.json()

    def getUpdates(self):
        localURL = self.URL + 'getupdates'
        r = requests.get(localURL)
        return r.json()

    def getLastUpdate(self):

        try:
            return self.getUpdates()['result'][-1]
        except IndexError as e:
            pass

    def getLastMessageId(self):

        return int(self.getLastUpdate()['message']['message_id'])

    def sendMessageLS(self, chat_id, text):
        try:
            localURL = self.URL + 'sendMessage?chat_id='+ str(chat_id) + '&text=' + str(text)
            requests.get(localURL)
        except Exception as e:
            file = open('errors.txt', 'a')
            file.write('\n1. ' + str(e))

    def sendMessageALL(self, text):
        try:
            data = self.jsonFromFile()
            for x in data:
                self.sendMessageLS(data[x], text)
        except Exception as e:
            pass
           

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

    def addChatIdIfNew(self, chat_id):

        chat_id = str(chat_id)

        if chat_id not in str(self.chat_id_list):

            self.chat_id_list.append(chat_id)

            data = {}
            for i in range(len(self.chat_id_list)):
                data[i+1] = self.chat_id_list[i]
            print(data)
            with open('interlocutors.json', 'w') as outfile:
                json.dump(data, outfile)

    def getLastMessage(self, chat_id):

        data = self.getUpdates()['result']
        data.reverse()
        message = 'not found'
        for x in data:
            if x['message']['chat']['id'] == chat_id:
                message = x['message']['text']
                break

        return str(message)

    def getChatId(self, message_id):

        data = self.getUpdates()['result']
        data.reverse()
        chatid = 0
        for x in data:
            if x['message']['message_id'] == message_id:
                chatid = x['message']['chat']['id']
                break

        return chatid
    
    def function(self, chat_id, message):

        if message == '/help':
            self.sendMessageLS(chat_id, 'use /translate < what to translate > and all will translated on Russian language!')

        elif message == '/start':
            self.sendMessageLS(chat_id, 'Hi ! Read /help and goodluck!')

        elif '/translate' in message:
                self.sendMessageLS(chat_id, self.translateYandex(message[11:]))

        elif message == '/restartbot':
            self.sendMessageLS(chat_id, 'W8 I start restarted!')
            os.system("python3 restart.py")
            sys.exit()
        else:
            self.sendMessageLS(chat_id, 'I don\'t know what u want =/')
    
    def isNewMessage(self):

        try:
            lastMessage_id = self.getLastUpdate()['update_id']
            newMessage_id = self.getLastUpdate()['update_id']

            while newMessage_id == lastMessage_id:
                data = self.getLastUpdate()
                newMessage_id = data['update_id']

            message_id = data['message']['message_id']

            return True, message_id

        except Exception as e:
            pass

    def jsonFromFile(self):

        try:
            with open ('interlocutors.json') as f:
                data = json.load(f)

            return data

        except Exception as e:
            pass
          
    def Online(self):

        self.sendMessageALL('Bot was restarted!')

        while True:
            try:
                isnew = self.isNewMessage()
                if (isnew[0]):
                    chat_id = self.getChatId(isnew[1])
                    message = self.getLastMessage(chat_id)
                    self.function(chat_id, message)
                    self.addChatIdIfNew(chat_id)

            except IndexError:
                continue

def main():
    bot = Telegram(token)
    bot.Online()

if __name__ == '__main__':
    main()