from dictionary import Dictionary
from config.settings import (token, lang)
from MySQLdb import _mysql
import telebot
import sys
import random

bot = telebot.TeleBot(token)
d = Dictionary(lang)

class Database():
    def __init__(self):
        self.host = host
        self.port = port
    
    def stablish_connection(self):
        db=_mysql.connect(host="localhost",user="joebob",
                  passwd="moonpie",db="thangs")
class Messages():
    def __init__(self, msg):
        self.msg = msg
        self.reply_message = 'error'

    def get_random_translation(self):
        n_key = random.randint(0,len(d.dictionary_json.keys()))
        selected_key = list(d.dictionary_json.keys())[n_key]
        self.reply_message = '%s => %s' % (selected_key, d.dictionary_json[selected_key])


    def edit_translation(self):
        rows = self.msg.split('\n')
        for row in rows:
            translation = row.replace('**', '').split('-')
            d.dictionary_json[translation[0].lower()] = translation[1].lower()
            d.update_dictionary()
            self.reply_message = "Updated!"

    def analyze_message(self):
        try:
            if self.msg == 'random':
                self.get_random_translation()
            elif '**' in self.msg:
                self.edit_translation()
            else:
                self.reply_message = d.dictionary_json[self.msg.lower()]
        except Exception as e:
            print("Exception (analyze_message) -> ", str(e))
            pass

        return self.reply_message


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    message.text = message.text.lower()
    msg = 'err'
    try:
        if message.text == 'random':
            n_key = random.randint(0,len(d.dictionary_json.keys()))
            selected_key = list(d.dictionary_json.keys())[n_key]
            msg = '%s => %s' % (selected_key, d.dictionary_json[selected_key])
        elif '**' in message.text:
            rows = message.text.split('\n')
            for row in rows:
                translation = row.replace('**', '').split('-')
                d.dictionary_json[translation[0].lower()] = translation[1].lower()
                d.update_dictionary()
                msg = "Updated!"
        else:
            msg = d.dictionary_json[message.text.lower()]
    except Exception as e:
        print("Exception (echo_all) -> ", str(e))
        pass
    
    bot.reply_to(message,msg)

bot.polling()