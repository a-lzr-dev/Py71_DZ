from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views

app_name = "notes:api"

notes_router = DefaultRouter()
notes_router.register("notes", views.NoteViewSet, basename="notes")
# /api/notes/       GET    - LIST
# /api/notes/       POST   - CREATE
# /api/notes/<id>/  GET    - DETAIL VIEW
# /api/notes/<id>/  PUT    - UPDATE
# /api/notes/<id>/  PATCH  - PATCH
# /api/notes/<id>/  DELETE - DELETE

notes_router.register("comments", views.CommentViewSet, basename="comments")
# /api/comments/       GET    - LIST
# /api/comments/?note=123   GET    - LIST
# /api/comments/       POST   - CREATE  { "note": 123, "text": "..." }
# /api/comments/<id>/  GET    - DETAIL VIEW
# /api/comments/<id>/  PUT    - UPDATE
# /api/comments/<id>/  PATCH  - PATCH
# /api/comments/<id>/  DELETE - DELETE


# ================================================================================
comments_nested_router = NestedDefaultRouter(notes_router, "notes", lookup="note")
comments_nested_router.register("comments", views.CommentViewSet, basename="note-comments")

# /api/notes/<note_id>/comments/       GET     - LIST        (comments)
# /api/notes/<note_id>/comments/       POST    - CREATE      (comments)   { "text": "..." }
# /api/notes/<note_id>/comments/<pk>/  GET     - DETAIL VIEW (comments)
# /api/notes/<note_id>/comments/<pk>/  PUT     - UPDATE      (comments)
# /api/notes/<note_id>/comments/<pk>/  PATCH   - PATCH       (comments)
# /api/notes/<note_id>/comments/<pk>/  DELETE  - DELETE      (comments)
