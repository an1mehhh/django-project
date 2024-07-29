from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта', primary_key=True)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    email_verification = models.CharField(max_length=64, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
