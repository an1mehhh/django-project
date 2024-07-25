from django.db import models

from mailing.models import Mailing

NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class Message(models.Model):
    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', on_delete=models.CASCADE)
    subject = models.CharField(verbose_name='Тема письма', max_length=255)
    body = models.TextField(verbose_name='Тело письма', blank=True, null=True)

    def __str__(self):
        return self.subject
