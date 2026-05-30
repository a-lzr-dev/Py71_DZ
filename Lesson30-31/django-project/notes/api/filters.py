from django.contrib.postgres.search import TrigramSimilarity, SearchRank, SearchQuery
from django.db.models import F, Q
from django_filters import rest_framework as drf_filters

from notes.models import Note, Comment


class NoteFilter(drf_filters.FilterSet):
    search = drf_filters.CharFilter(method="fts_search", label="Full text search")
    username = drf_filters.CharFilter(field_name="user__username", label="Username")
    # tags = drf_filters.ModelMultipleChoiceFilter(
    #     field_name="tags__name", queryset=Tag.objects.all(), to_field_name="name"
    # )
    tags = drf_filters.CharFilter(method="tags_filter", label="Tags")
    time = drf_filters.DateFromToRangeFilter(field_name="created_at", label="By created at field")

    class Meta:
        model = Note
        fields = ["search", "username", "tags", "time"]

    @staticmethod
    def fts_search(queryset, name: str, value: str):
        value = value.strip()
        if not value:
            return queryset

        vector_query = SearchQuery(value, config="russian", search_type="websearch")
        queryset = queryset.filter(Q(search_vector=vector_query) | Q(title__trigram_similar=value))
        queryset = queryset.annotate(
            rank=SearchRank(F("search_vector"), vector_query),
            trigram=TrigramSimilarity("title", value),
        )
        return queryset.order_by("-rank", "-trigram", "-created_at")

    @staticmethod
    def tags_filter(queryset, name: str, value: str):
        value = value.strip()
        if not value:
            return queryset

        return queryset.filter(tags__name=value)


class CommentFilter(drf_filters.FilterSet):
    text = drf_filters.CharFilter(lookup_expr="icontains")
    username = drf_filters.CharFilter(field_name="user__username", label="Username")
    time = drf_filters.DateFromToRangeFilter(field_name="created_at", label="By created at field")

    class Meta:
        model = Comment
        fields = ["text", "username", "time", "note_id"]
