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

"""
class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class EventSerializer(serializers.ModelSerializer):
#    user = UserShortSerializer(read_only=True)
#    tags = serializers.ListSerializer(child=serializers.CharField(), read_only=True)
#    image = serializers.CharField(required=False)

    class Meta:
        model = Event
        fields = ["id", "name", "meeting_time", "description"]
#        read_only_fields = ["id", "user", "created_at", "updated_at"]


#class EventListSerializer(serializers.ModelSerializer):
#    user = UserShortSerializer(read_only=True)
#    tags = serializers.ListSerializer(child=serializers.CharField(), read_only=True)
#    description_preview = serializers.CharField(read_only=True)

#    class Meta:
#        model = Event
#        fields = ["id", "name"]

"""