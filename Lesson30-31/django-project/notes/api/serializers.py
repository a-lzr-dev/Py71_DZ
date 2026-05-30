from rest_framework import serializers

from accounting.models import User
from notes.models import Note, Comment


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class NoteSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    tags = serializers.ListSerializer(child=serializers.CharField(), read_only=True)
    image = serializers.CharField(required=False)

    class Meta:
        model = Note
        fields = ["id", "title", "content", "user", "image", "created_at", "updated_at", "tags"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class NoteListSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    tags = serializers.ListSerializer(child=serializers.CharField(), read_only=True)
    content_preview = serializers.CharField(read_only=True)

    class Meta:
        model = Note
        fields = ["id", "title", "content_preview", "user", "image", "created_at", "updated_at", "tags"]


class NoteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title']


class CommentNoteWriteSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "text", "user", "note", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "text", "user", "note", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "note", "created_at", "updated_at"]
