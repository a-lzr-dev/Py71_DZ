from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass

@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    from .tasks import welcome_email_sender

    if created:
        welcome_email_sender.delay(instance.id)