from django.db import models

from users.models import User

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    PERIODICITY_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    start_time = models.DateTimeField(verbose_name='Время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Время окончания рассылки')
    periodicity = models.CharField(max_length=10, verbose_name='Периодичность рассылки', choices=PERIODICITY_CHOICES)
    status = models.CharField(max_length=10, verbose_name='Статус рассылки', choices=STATUS_CHOICES, default='created')
    recipients = models.TextField(verbose_name='Список получателей',
                                  help_text='Введите адреса электронной почты через запятую', default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.owner:
            self.owner = self.request.user
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Mailing {self.id} - {self.status}"

