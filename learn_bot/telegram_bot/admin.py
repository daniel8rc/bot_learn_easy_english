from django.contrib import admin
from telegram_bot.models import (tDictionary,)
from django import forms
from django.conf import settings


class tDictionaryAdmin(admin.ModelAdmin):

    readonly_fields = [
        'english_text',
        'spanish_text',
    ]


admin.site.register(tDictionary, tDictionaryAdmin)
admin.site.site_header = ('Telegram Bot')
admin.site.site_url = '/main'
