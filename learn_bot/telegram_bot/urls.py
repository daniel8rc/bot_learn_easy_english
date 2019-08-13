from django.urls import (re_path, path)
from . import views

app_name = 'telegram_bot'
urlpatterns = [
    r'dictionary/(.*)',
        views.dictionary,
        name="dictionary"
    ),
]