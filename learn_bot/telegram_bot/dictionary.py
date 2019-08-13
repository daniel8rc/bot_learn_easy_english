#!/usr/bin/python
# -*- coding: utf-8 -*-

from translate import Translator
import urllib.request
import numpy as np
import json
import os
import time
import glob

resources_path = 'resources/files/'

class TranslatorText():
    def __init__(self, lang):
        self.lang = lang
        self.translator= Translator(to_lang=lang)

    def translate_text(self, t_translate):
        translation = ''
        try:
            translation = self.translator.translate(t_translate)
        except Exception as e:
            print("Error translate (translate_text) -> ", str(e))
        return translation

class Dictionary(TranslatorText):
    def __init__(self, lang):       
        self.name_dictionary = 'dictionary_%s.json' % (lang.lower())
        self.dictionary_json = self.load_dictionary()
        super().__init__(lang)
    
    def update_dictionary(self):
        with open(resources_path + self.name_dictionary, 'w', encoding='utf8') as outfile:
            json.dump(self.dictionary_json, outfile, ensure_ascii=False)


    def check_in_dictionary(self, word):
        found = False
        if word in self.dictionary_json and '' != self.dictionary_json[word] and 'usagelimits' not in self.dictionary_json[word]:
            found = True
        else:
            print("Translate --> ", self.dictionary_json['word'])
        found = True
        return found

    def load_dictionary(self):
        dictionary_json = {}
        with open(resources_path + self.name_dictionary) as json_file:
            dictionary_json = json.load(json_file)
        return dictionary_json
    
    def load_file_text(self, file_name):
        """
        Example with file_name="words_en.txt"
        """
        f_text = np.loadtxt(fname=file_name, dtype='str', delimiter="\n")
        return f_text

    def get_files_translations(self):
        return glob.glob("%stranslations/*.txt" % (resources_path))

    def add_new_translations(self):
        files = self.get_files_translations()
        for f in files:
            f_text = self.load_file_text(f)
            for translation in f_text:
                t = translation.split('**')
                

    def add_new_words(self, file_name):
        f_text = self.load_file_text(resources_path + file_name)
        print(f_text)
        for word in f_text:
            if not self.check_in_dictionary(word):
                translation = self.translate_text(word)
                self.dictionary_json[word] = translation.lower()
                self.update_dictionary()


if __name__ == '__main__':
    d =  Dictionary("Spanish")
    #d.add_new_words("words_en.txt")
    d.add_new_translations()

