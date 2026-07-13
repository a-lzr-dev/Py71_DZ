from django.db import models

from accounting.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reminder_day_sent = models.BooleanField(default=False)   # отправлено уведомление за день
    reminder_hour_sent = models.BooleanField(default=False)  # отправлено уведомление за 6 часов

    class Meta:
        unique_together = ('user', 'event')

@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
def event_post_save(sender, created, instance, **kwargs):
    from .tasks import send_notifies_on_new, clear_cached_events

    if created:
        send_notifies_on_new.delay(instance.id)

    clear_cached_events() # очистка кэша