from dictionary import Dictionary
from config.settings import (token, lang)
import telebot
import sys
import random
bot = telebot.TeleBot(token)
d = Dictionary(lang)

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
            print("Edita")
            message.text = message.text.replace('**edit**', '')
            translation = message.text.split('-')
            d.dictionary_json[translation[0]] = translation[1].lower()
            d.update_dictionary()
            msg = "Updated!"
        else:
            msg = d.dictionary_json[message.text.lower()]
    except Exception as e:
        print("Exception (echo_all) -> ", str(e))
        pass
    
    bot.reply_to(message,msg)

bot.polling()