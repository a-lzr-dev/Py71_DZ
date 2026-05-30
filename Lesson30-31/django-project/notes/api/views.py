from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Substr
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from notes.models import Note, Comment
from .filters import NoteFilter, CommentFilter
from .permissions import IsNoteAndCommentOwnerOrReadOnly
from .serializers import NoteSerializer, NoteListSerializer, CommentNoteWriteSerializer, CommentSerializer, \
    NoteHistorySerializer
from ..services import NotesCache

session_key = "read_notes"

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def notes_api_view(request):
    if request.method == "GET":
        notes = Note.objects.all()[:10]
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    else:
        print("request.data:", request.data)
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save(user=request.user)  # create new note
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def note_detail_api_view(request, note_id: int):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "DELETE":
        note.delete()
        return Response(NoteSerializer(note).data, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = NoteSerializer(note, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # update
        return Response(NoteSerializer(note).data)

    elif request.method == "PATCH":
        serializer = NoteSerializer(note, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(NoteSerializer(note).data)

    # method == "GET"
    return Response(NoteSerializer(note).data)


class NoteListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = NoteFilter
    queryset = (
        Note.objects.all()
        .select_related("user")
        .prefetch_related("tags")
        .only(
            "title",
            "user",
            "image",
            "created_at",
            "updated_at",
            "user__username",
            "user__email",
        )
        .annotate(content_preview=Substr("content", 1, 200))
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return NoteListSerializer
        return NoteSerializer


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsNoteAndCommentOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "note_id"
    queryset = (
        Note.objects.all()
        .select_related("user")
        .only(
            "title",
            "user",
            "image",
            "content",
            "created_at",
            "updated_at",
            "user__username",
            "user__email",
        )
    )
    serializer_class = NoteSerializer


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    permission_classes = [IsAuthenticatedOrReadOnly, IsNoteAndCommentOwnerOrReadOnly]
    filterset_class = NoteFilter
    cache_list_timeout = 60

    def get_queryset(self):
        if self.action == "list":
            return (
                Note.objects.all()
                .select_related("user")
                .prefetch_related("tags")
                .only(
                    "title",
                    "user",
                    "image",
                    "created_at",
                    "updated_at",
                    "user__username",
                    "user__email",
                )
                .annotate(content_preview=Substr("content", 1, 200))
            )
        return Note.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return NoteListSerializer
        return NoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "favorite":
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        notes_cache = NotesCache(request)

        if notes_cache.can_use_cache:
            cached_data = notes_cache.get()
            if cached_data is not None:
                return Response(cached_data)

        new_response = super().list(request, *args, **kwargs)

        notes_cache.set(new_response.data)

        return new_response

    def retrieve(self, request, *args, **kwargs):
        # переопределение retrieve, чтобы сохранить ID заметки в историю
        response = super().retrieve(request, *args, **kwargs)
        history = request.session.get(session_key, [])
        note_id = kwargs.get('id')
        if note_id in history:
            history.remove(note_id)

        history.append(kwargs.get('id'))
        if len(history) > 20:
            history.pop(0)
        request.session[session_key] = history

        return response

    @action(detail=True, methods=["POST", "DELETE"])
    def favorite(self, request, pk=None):
        note = self.get_object()

        # Добавление в избранное.
        print("Добавление в избранное: ", note)
        # =======================

        if self.request.method == "DELETE":
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='history')
    def history(self, request):
        # возвращает просмотренные заметки
        history_ids = request.session.get(session_key, [])
        notes = []
        for note_id in history_ids:
            try:
                note = Note.objects.get(id=note_id)
                notes.append(note)
            except ObjectDoesNotExist:
                continue
        serializer = NoteHistorySerializer(notes, many=True)
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsNoteAndCommentOwnerOrReadOnly]
    filterset_class = CommentFilter
    # default: lookup_url_kwarg = "pk"
    # default: lookup_field = "pk"

    def get_queryset(self):
        qs = Comment.objects.all().select_related("user")

        note_id = self.kwargs.get("note_id")
        if note_id is not None:
            return qs.filter(note_id=note_id)

        return qs

    def get_serializer_class(self):
        if self.kwargs.get("note_id") is not None:
            return CommentSerializer
        return CommentNoteWriteSerializer

    def perform_create(self, serializer):
        if self.kwargs.get("note_id") is not None:
            note = get_object_or_404(Note, pk=self.kwargs["note_id"])
            serializer.save(user=self.request.user, note=note)

        else:
            serializer.save(user=self.request.user)
