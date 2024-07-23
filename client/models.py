from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class Client(models.Model):
    email = models.EmailField(verbose_name='Почта', unique=True)
    full_name = models.CharField(verbose_name='Полное имя клиента', max_length=100)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return self.full_name
