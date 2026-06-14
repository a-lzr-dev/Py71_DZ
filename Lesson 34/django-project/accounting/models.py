from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    notify = models.BooleanField(default=True, verbose_name="Подписка на рассылку")
