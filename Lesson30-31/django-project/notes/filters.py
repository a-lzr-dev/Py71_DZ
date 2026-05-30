from datetime import datetime

from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q, QuerySet
from django.db.models.functions import Substr

from accounting.models import User
from .models import Note, Tag


def filter_notes_list(
    search: str = "",
    user: User | None = None,
    tags: QuerySet[Tag] | None = None,
    time_gt: datetime | None = None,
) -> QuerySet[Note]:
    notes_qs = Note.objects.all()
    if search:
        vector_query = SearchQuery(search, config="russian", search_type="websearch")
        notes_qs = notes_qs.filter(Q(search_vector=vector_query) | Q(title__trigram_similar=search))
        notes_qs = notes_qs.annotate(
            rank=SearchRank(F("search_vector"), vector_query),
            trigram=TrigramSimilarity("title", search),
        )
        notes_qs = notes_qs.order_by("-rank", "-trigram", "-created_at")

    if user:
        notes_qs = notes_qs.filter(user=user)

    if tags:
        notes_qs = notes_qs.filter(tags__in=tags)

    if time_gt:
        notes_qs = notes_qs.filter(created_at__gt=time_gt)

    notes_qs = notes_qs.select_related("user")  # JOIN с users только для FK.
    notes_qs = notes_qs.prefetch_related("tags")  # JOIN только для M2M.
    notes_qs = notes_qs.annotate(short_content=Substr("content", 1, 200))
    notes_qs = notes_qs.only("id", "title", "updated_at", "user__username")

    return notes_qs
