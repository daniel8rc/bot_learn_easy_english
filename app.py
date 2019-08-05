import json
import os
import numpy as np
import urllib.request
from googletrans import Translator

resources_path = 'resources/files/'


class Dictionary():
    def __init__(self):
        self.name_dictionary = 'dictionary.json'
        self.dictionary_json = self.load_dictionary()
    
    def update_dictionary(self):
        
        with open(resources_path + self.name_dictionary, 'w') as outfile:
            json.dump(self.dictionary_json, outfile)

    def check_in_dictionary(self, word):
        found = False
        if word not in self.dictionary_json:
            found = True
        return found

    def load_dictionary(self):
        with open(resources_path + self.name_dictionary) as json_file:
            self.dictionary_json = json.load(json_file)
    
    def load_file_text(self, file_name):


    def add_new_words(self, file_name)
