from django.db import models

from accounting.models import User

CATEGORY_CHOICES = [
    ('dance', 'Танцы'),
    ('party', 'Вечеринка'),
    ('hike', 'Поход'),
    ('other', 'Другое'),
]

class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название события")
    description = models.TextField(blank=True, verbose_name="Описание события")
    city = models.CharField(max_length=100, default='Минск', verbose_name='Город')
    meeting_time = models.DateTimeField(verbose_name="Дата и время проведения")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name='Категория')
    users = models.ManyToManyField(User, related_name='events', blank=True, verbose_name='Участники')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['meeting_time']

