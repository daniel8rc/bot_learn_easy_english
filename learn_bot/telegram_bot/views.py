from django.shortcuts import render
from .models import tDictionary
from rest_framework import (permissions, response, generics, status)
from rest_framework.response import Response

# Create your views here.

class DictionaryController(generics.GenericAPIView):
    def get(self, option):
        self.response = {}
        self.response['status'] = 400
        self.status_response = status.HTTP_400_BAD_REQUEST

        try:
            if option == 'reload':
                self.status_response = status.HTTP_200_OK
                self.response['status'] = 200
        except:
            pass
        
        return Response(self.response, status=self.status_response)


dictionary = DictionaryController.as_view()