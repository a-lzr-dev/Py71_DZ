from django.core.cache import cache

from notes.models import Note, NoteReaction


def set_note_reaction(note: Note, user, reaction: str) -> None:
    status = NoteReaction.objects.filter(note=note, user=user).update(reaction=reaction)
    # Если уже была реакция.
    if status:
        return

    NoteReaction.objects.create(note=note, user=user, reaction=reaction)


class NotesCache:
    cache_timeout = 120
    max_page_cache_size = 10
    cache_key_prefix = "api:notes:list:page"

    def __init__(self, request) -> None:
        self.request = request
        self._page = self._get_page()
        self.can_use_cache = (
            self._page is not None
            and 0 < self._page <= self.max_page_cache_size
            and not self.has_other_query_params
        )

    @property
    def has_other_query_params(self) -> bool:
        return bool([key for key, value in self.request.GET.items() if key != "page" and value])

    def get(self) -> dict | None:
        return cache.get(self._get_cache_key())

    def set(self, data) -> None:
        cache.set(self._get_cache_key(), data, self.cache_timeout)

    @classmethod
    def clear_cache(cls) -> None:
        for i in range(cls.max_page_cache_size):
            cache.delete(f"{cls.cache_key_prefix.rstrip(":")}:{i}")

    def _get_page(self) -> int | None:
        page_raw = self.request.GET.get("page", "1")
        if page_raw.isdigit():
            return int(page_raw)
        return None

    def _get_cache_key(self):
        return f"{self.cache_key_prefix.rstrip(":")}:{self._page}"
