from rest_framework import serializers

from accounting.api.serializers import UserSerializer
from accounting.models import User
from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'meeting_time', 'description', 'users']
        read_only_fields = ['id']