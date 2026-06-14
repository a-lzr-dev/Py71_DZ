from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Event
from accounting.models import User

REMINDER_ON_ADD = 0
REMINDER_BEFORE_DAYS = 1 # оповещение за указанное число дней
REMINDER_BEFORE_HOURS = 2 # оповещение за указанное число часов

reminders = [
    (REMINDER_BEFORE_DAYS, 1), # за 1 день
    (REMINDER_BEFORE_HOURS, 6), # за 6 часов
]

@shared_task(queue='email_queue')
def send_email_task(subject, message, recipient_list):
    # отправка письма по электронной почте
    send_mail(subject, message, settings.EMAIL_HOST_USE, recipient_list)

@shared_task()
def send_event_reminder(event_id, user_email, reminder_type, reminder_period = 0):
    # настройка текста уведомления и вызов отправки
    try:
        event = Event.objects.get(id=event_id)
        if reminder_type == REMINDER_ON_ADD:
            subject = f'Новое мероприятие: "{event.name}"'
            message = (
                f'Новое мероприятие: "{event.name}".\n'
                f'{event.description}\n'
                f'Мероприятие проходит {event.meeting_time.strftime("%d.%m.%Y в %H:%M")} {event.city}.'
            )
        elif reminder_type == REMINDER_BEFORE_DAYS & reminder_period == 1:
            subject = f'Завтра начнется "{event.name}"'
            message = (
                f'Уведомляем вас, что вы согласились посетить "{event.name}".\n'
                f'{event.description}\n'
                f'Мероприятие проходит завтра в {event.meeting_time.strftime("%H:%M")} {event.city}.'
            )
        elif reminder_type == REMINDER_BEFORE_DAYS:
            subject = f'Через {reminder_period} дней начнется "{event.name}"'
            message = (
                f'Уведомляем вас, что вы согласились посетить "{event.name}".\n'
                f'{event.description}\n'
                f'Мероприятие начнется через {reminder_period} дней в {event.meeting_time.strftime("%H:%M")} {event.city}.'
            )
        elif reminder_type == REMINDER_BEFORE_HOURS:
            subject = f'Через {reminder_period} часов начнется "{event.name}"'
            message = (
                f'Уведомляем вас, что вы согласились посетить "{event.name}".\n'
                f'{event.description}\n'
                f'Мероприятие начнется через {reminder_period} часов в {event.meeting_time.strftime("%H:%M")} {event.city}.'
            )
        else:
            raise ValueError(f"Неизвестный тип уведомления: {reminder_type}")

        send_email_task(subject, message, [user_email])

    except Event.DoesNotExist:
        pass

@shared_task()
def send_notifies_on_new(event_id):
    # отправка оповещения при добавлении нового события только пользователям с подпиской
    event = Event.objects.get(id=event_id)
    users = User.objects.filter(notify=True)
    for user in users:
        send_event_reminder.delay(event.pk, user.email, REMINDER_ON_ADD)

@shared_task
def send_notifies_by_scheduler():
    # отправка оповещений согласно расписания
    now = timezone.now()

    for rtype, interval in reminders:
        if rtype == REMINDER_BEFORE_DAYS:
            event_start = now + timedelta(days=interval)
        elif rtype == REMINDER_BEFORE_HOURS:
            event_start = now + timedelta(hours=interval)
        else:
            continue

        events = Event.objects.filter(
            meeting_time__date=event_start.date()
        )
        for event in events:
            for user in event.users.all():
                send_event_reminder.delay(event.pk, user.email, rtype, interval)

@shared_task
def get_cached_events():
    # кэширование всех событий на 5 мин
    events = cache.get('all_events')
    if not events:
        events = list(Event.objects.select_related().all())
        cache.set('all_events', events, 60 * 5)
    return events

def clear_cached_events():
    # очистка кэша
    cache.delete('all_events')