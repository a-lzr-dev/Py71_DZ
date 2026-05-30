from django import forms

from accounting.models import User
from .models import Note, Comment, Tag, NoteReaction


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "image", "tags"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }


class NotesSearchForm(forms.Form):
    search = forms.CharField(max_length=200, required=False, label="Поиск")
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label="Пользователи")
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, label="Теги")
    time_gt = forms.DateTimeField(required=False, label="Дата и время создания старше")


class NoteReactionForm(forms.ModelForm):
    class Meta:
        model = NoteReaction
        fields = ["reaction"]
