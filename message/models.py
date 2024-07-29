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


class Log(models.Model):
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE, related_name='logs')
    attempt_time = models.DateTimeField(verbose_name='Дата и время последней отправки', auto_now=True)
    status = models.CharField(verbose_name='Статус', max_length=50)
    server_response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)

    def str(self):
        return f"Log {self.id} - {self.status}"
