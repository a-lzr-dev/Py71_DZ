from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.NotesListView.as_view(), name="list"),
    path("create", views.NoteCreateView.as_view(), name="create"),
    path("<int:note_id>", views.note_detail_view, name="detail"),
    path("<int:note_id>/create-comment", views.create_note_comment_view, name="create-comment"),
    path("<int:note_id>/set-reaction", views.set_note_reaction_view, name="set-reaction"),
]
