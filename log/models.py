from django.db import models

from mailing.models import Mailing
from message.models import Message

NULLABLE = {'blank': True, 'null': True}

# Create your models here.


class Log(models.Model):
    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', on_delete=models.CASCADE, **NULLABLE)
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(verbose_name='Дата и время последней отправки', auto_now=True)
    status = models.CharField(verbose_name='Статус', max_length=50)
    server_response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f"Log {self.id} - {self.status}"
