#!/usr/bin/python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from learn_bot.config.settings import (dictionary_path)
from rest_framework import (permissions, response, generics, status)
from rest_framework.response import Response
from .dictionary import Dictionary as D
import time

# Create your views here.

class DictionaryApiController(generics.GenericAPIView):
    def reload_dictionary(self):
        print(dictionary_path)
        d =  D(dictionary_path)

        d.add_new_translations()

    def get(self, request, option):
        self.response = {}
        self.response['status'] = 400
        self.status_response = status.HTTP_400_BAD_REQUEST

        try:
            if option == 'reload':
                self.reload_dictionary()
                self.status_response = status.HTTP_200_OK
                self.response['status'] = 200
        except:
            pass
        print ("\n\nerror____")
        print("_...__")
        time.sleep(2)
        return Response(self.response, status=self.status_response)


dictionary = DictionaryApiController.as_view()