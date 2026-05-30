from django.apps import AppConfig
from django.db.models.signals import post_save


class NotesConfig(AppConfig):
    name = "notes"

    def ready(self):
        from .models import Note
        from notes.services import NotesCache

        def post_save_note_signal(sender, instance, created: bool, **kwargs):
            if created:
                NotesCache.clear_cache()

        post_save.connect(
            post_save_note_signal, sender=Note, weak=False, dispatch_uid="post_save_note_signal"
        )
