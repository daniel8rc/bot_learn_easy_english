from django.db import models

# Create your models here.

class Dictionary(models.Model):
    """
    Dictionary model.
    """

    english_text = models.CharField(max_length=255, unique=True)
    spanish_text = models.CharField(max_length=255)


    def __str__(self):
        return 'English %s -> Spanish %s.' % (self.english_text, self.spanish_text)

    class Meta:
        verbose_name = 'Dictionary'
        managed = True
        db_table = 'tDictionary'