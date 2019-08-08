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

USERS = {

}
COMMANDS_BOT = ['start_letter_game', 'show_hint', 'stop_letter_game', 'show_score']

class Database():
    def __init__(self):
        self.host = host
        self.port = port
    
    def stablish_connection(self):
        db =_mysql.connect(host="localhost",user="joebob",
                  passwd="moonpie",db="thangs")

class Messages():
    def __init__(self, message):
        self.original_message = message
        self.msg = message.text
        self.reply_message = ''
        self.chat_id = message.chat.id
        self.create_user()

    def show_answer_box(self, responses, title_box):
        markup = types.ReplyKeyboardMarkup(row_width=len(responses))

        for response in responses:
            markup.add(
                types.KeyboardButton('/' + response)
            )
        bot.send_message(self.chat_id, title_box, reply_markup=markup)
        
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

    def send_reply(self, message):
        if self.reply_message:
            bot.reply_to(message, self.reply_message)
    
    def analyze_message(self):
        try:
            if USERS[self.chat_id]['in_action'] == 'letter_game':
                lg = LetterGame(self.original_message)
                lg.analyze_reply_message()
                lg.update_game()
            
            elif self.msg == 'random':
                selected_key = self.get_random_translation()
                self.reply_message = '%s => %s' % (selected_key, d.dictionary_json[selected_key])
            elif '**' in self.msg:
                self.edit_translation()
            else:
                print("Translate")
                self.reply_message = d.dictionary_json[self.msg.lower()]

        except Exception as e:
            print("Exception (analyze_message) -> ", str(e))
            pass

        return self.reply_message

    def create_user(self):
        if not self.chat_id in USERS:
            USERS[self.chat_id] = {}
            USERS[self.chat_id]['in_action'] = None
            USERS[self.chat_id]['games'] = {}
            USERS[self.chat_id]['games']['letter_game'] = {}
            USERS[self.chat_id]['games']['letter_game']['scores'] = {
                'win': 0,
                'lose': 0
            }


class LetterGame(Messages):
    def __init__(self, message):
        self.chat_id = message.chat.id
        self.username = message.chat.username
        self.original_message = message
        self.create_user()
            

        self.letter_game = USERS[self.chat_id]['games']['letter_game']
        super().__init__(message)

    def new_game(self):
        USERS[self.chat_id]['in_action'] = 'letter_game'
        self.letter_game['lives'] = 5
        self.letter_game['selected_word'] = ''

    def stop(self):
        USERS[self.chat_id]['in_action'] = None
        self.message = "Stopped letter game"
        self.show_message()

    def show_hint(self):
        selected_word = self.letter_game['selected_word']
        word = list(selected_word)
        np.random.shuffle(word)
        self.message = ' '.join(word)
        self.show_message()

    def show_message(self):
        bot.send_message(self.chat_id, self.message)

    def show_score(self):
        self.message = "Score Letter Game %s\n" % (self.username)
        self.message += "Win: %i 👍🏼 Lose: %i 👎" % (
            self.letter_game['scores']['win'],
            self.letter_game['scores']['lose']
        )
        self.show_message()
        

    def analyze_reply_message(self):
        if self.msg == self.letter_game['selected_word']:
            self.message = 'You win!!'
            self.show_message()
            self.letter_game['scores']['win'] += 1
            self.stop()
        else:
            self.letter_game['lives'] -= 1
            if self.letter_game['lives'] > 0:
                self.message = "Isn't correct. Lives: "
                for l in range(0, self.letter_game['lives']):
                    self.message += "️❤️"
                self.show_message()
            else:
                self.message = "You louse 😔. The word was '%s'." % (self.letter_game['selected_word'])
                self.show_message()
                self.letter_game['scores']['lose'] += 1
                self.stop()

    def play(self):
        print("In play!!")
        if not self.letter_game['selected_word']:
            selected_word = self.get_random_translation()
        else:
            selected_word = self.letter_game['selected_word']
        
        self.letter_game['selected_word'] = selected_word
        translation = d.dictionary_json[selected_word]
        self.message = "Translation: %s\n" % (translation)
        for ch in range(len(selected_word)):
            if not self.message:
                self.message = '_'
            else:
                self.message += ' _'
        print(self.message)
        self.show_message()
    
    def update_game(self):
        USERS[self.chat_id]['games']['letter_game'] = self.letter_game



@bot.message_handler(commands=COMMANDS_BOT)
def start_game(message):
    print("Entra!")
    lg = LetterGame(message)
    if message.text == '/start_letter_game':
        lg.new_game()
        lg.play()
        lg.show_answer_box(
            COMMANDS_BOT,
            "Select a option"
        )
    elif message.text == '/stop_letter_game':
        lg.stop()
    elif message.text == '/show_hint':
        lg.show_hint()
    elif message.text == '/show_score':
        lg.show_score()
    lg.update_game()

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    message.text = message.text.lower()
    m = Messages(message)
    m.analyze_message()
    m.send_reply(message)

bot.polling()