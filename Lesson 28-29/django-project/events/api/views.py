from django.db.models.functions import Substr
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView

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


'''

class EventViewSet(viewsets.ModelViewSet):
    """
    CRUD для событий.
    - Для неавторизованных доступно только чтение.
    - При создании события автоматически назначается текущий пользователь.
    - Изменять/удалять событие может только его создатель или администратор.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Для изменяющих действий требуется аутентификация
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.created_by and not request.user.is_staff:
            return Response({'detail': 'У вас нет прав на удаление этого события.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.created_by and not request.user.is_staff:
            return Response({'detail': 'У вас нет прав на изменение этого события.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


"""
# from .filters import EventFilter
from .permissions import IsEventOwnerOrReadOnly
from .serializers import EventSerializer  # , EventListSerializer

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def events_api_view(request):
    if request.method == "GET":
        events = Event.objects.all()[:10]
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    else:
        print("request.data:", request.data)
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save(user=request.user)  # create new note
        return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def note_detail_api_view(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "DELETE":
        event.delete()
        return Response(EventSerializer(event).data, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = EventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # update
        return Response(EventSerializer(event).data)

    elif request.method == "PATCH":
        serializer = EventSerializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(EventSerializer(event).data)

    # method == "GET"
    return Response(EventSerializer(event).data)


class EventListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
#    filterset_class = EventFilter
    queryset = (
        Event.objects.all()
#        .select_related("user")
#        .prefetch_related("tags")
#         .only(
#             "name",
#             "meeting_time",
#             "description",
#         )
#        .annotate(description_preview=Substr("description", 1, 200))
    )

#    def perform_create(self, serializer):
#        serializer.save(user=self.request.user)

    def get_serializer_class(self):
#        if self.request.method == "GET":
#            return EventListSerializer
        return EventSerializer

class EventDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEventOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "event_id"
    queryset = (
        Event.objects.all()
#        .select_related("user")
        .only(
            "name",
            "meeting_time",
            "description",
        )
    )
    serializer_class = EventSerializer

#    def patch(self, request, *args, **kwargs):
#        super().patch(request, *args, **kwargs)
#        return Response(status=status.HTTP_200_OK)

"""
'''