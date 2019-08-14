#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .models import tDictionary
from translate import Translator
import urllib.request
import numpy as np
import json
import os
import time
import glob



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
    def __init__(self, resources_path):
        self.resources_path = resources_path
        self.lang = 'Spanish'
        self.dictionary_json = {}
        print("Init!")
        super().__init__(self.lang)

    def get_files_translations(self):
        return glob.glob("%s/*.txt" % (self.resources_path))

    def load_file_text(self, file_name):
        """
        Example with file_name="words_en.txt"
        """
        f_text = np.loadtxt(fname=file_name, dtype='str', delimiter="\n")
        return f_text

    def add_new_translations(self):
        print("Reloading translations...")
        files = self.get_files_translations()
        print("Total files to be read: ", len(files))
        for f in files:
            f_text = self.load_file_text(f)
            for translation in f_text:
                t = translation.split('**')
                td, created = tDictionary.objects.get_or_create(english_text=t[0])
                td.spanish_text = t[1]
                td.save()
                time.sleep(0.1)
            print("Finish ", f)



