from dictionary import Dictionary
from config.settings import (token, lang)
from MySQLdb import _mysql
import telebot
from telebot import types
import sys
import random
import numpy as np

bot = telebot.TeleBot(token)
d = Dictionary(lang)

games = {}

class Database():
    def __init__(self):
        self.host = host
        self.port = port
    
    def stablish_connection(self):
        db =_mysql.connect(host="localhost",user="joebob",
                  passwd="moonpie",db="thangs")

class GameLetters():
    def __init__(self, game_id):
        self.game_id = game_id
        self.message = ''
        if game_id not in games:
            games[game_id] = {
                'lives': 2,
                'in_game': False,
                'selected_word': ''
            }

    def play(self):
        selected_key = self.get_random_translation()
        games[self.game_id]
        self.message = '%s => %s\n' % (selected_key, d.dictionary_json[selected_key])
        letters_translate = list(d.dictionary_json[selected_key])
        
        np.random.shuffle(letters_translate)
        
        self.message = ' '.join(letters_translate)

class Messages(GameLetters):
    def __init__(self, msg):
        self.msg = msg
        self.reply_message = 'error'

    def get_random_translation(self):
        n_key = random.randint(0,len(d.dictionary_json.keys()))
        selected_key = list(d.dictionary_json.keys())[n_key]
        return selected_key
        


    def edit_translation(self):
        rows = self.msg.split('\n')
        for row in rows:
            translation = row.replace('**', '').split('-')
            d.dictionary_json[translation[0].lower()] = translation[1].lower()
            d.update_dictionary()
            self.reply_message = "Updated!"

    def play_game(self, game_id):
        
        g = GameLetters(game_id)
        g.play()

    def analyze_message(self):
        try:
            if self.msg == 'random':
                selected_key = self.get_random_translation()
                self.reply_message = '%s => %s' % (selected_key, d.dictionary_json[selected_key])
            elif '**' in self.msg:
                self.edit_translation()
            elif self.msg == 'game_words':
                self.play_game()
            else:
                self.reply_message = d.dictionary_json[self.msg.lower()]
        except Exception as e:
            print("Exception (analyze_message) -> ", str(e))
            pass

        return self.reply_message


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('hello')
    itembtn2 = types.KeyboardButton('good')
    itembtn3 = types.KeyboardButton('random')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

	# bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    message.text = message.text.lower()
    m = Messages(message.text)
    reply_message = m.analyze_message()
    bot.reply_to(message,reply_message)

bot.polling()