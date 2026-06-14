from django.db.models.functions import Substr
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView
from django.core.cache import cache

from ..models import Event
from .serializers import EventSerializer

class EventListView(ListAPIView):
    # Список всех предстоящих событий (требуется аутентификация)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return Event.objects.filter(meeting_time__gt=now)

class SubscribeToEventView(APIView):
    # Подписка на событие (только если событие ещё не началось)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        now = timezone.now()
        if event.meeting_time <= now:
            return Response(
                {"detail": "Нельзя подписаться на событие, которое уже началось."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.user in event.users.all():
            return Response(
                {"detail": "Вы уже подписаны на это событие."},
                status=status.HTTP_400_BAD_REQUEST
            )
        event.users.add(request.user)
        return Response({"detail": "Вы успешно подписались."}, status=status.HTTP_200_OK)

class MyEventsView(ListAPIView):
    # Список событий, на которые подписан текущий пользователь (только предстоящие)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return self.request.user.events.filter(meeting_time__gt=now)