from django.contrib.postgres.indexes import GinIndex, OpClass
from django.contrib.postgres.search import SearchVectorField
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

from project.helpers.models import AuditModel

USER_MODEL = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Note(AuditModel):
    user = models.ForeignKey(USER_MODEL, on_delete=models.RESTRICT)
    title = models.CharField(
        max_length=128,
        verbose_name="Заголовок",
        help_text="Не более 128 символов",
        validators=[MinLengthValidator(3)],
    )
    content = models.TextField(verbose_name="Содержимое")

    search_vector = SearchVectorField(null=True, editable=False)

    image = models.ImageField(
        upload_to="notes/%Y/%m", blank=True, null=True, verbose_name="Картинка", max_length=256
    )
    tags = models.ManyToManyField("Tag", blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            GinIndex(fields=["search_vector"], name="note_search_vector_gin"),
            GinIndex(OpClass("title", name="gin_trgm_ops"), name="note_title_trgm_gin"),
        ]


class Comment(AuditModel):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=1024, validators=[MinLengthValidator(3)], verbose_name="Комментарий")

    def __str__(self):
        return f"User: {self.user_id} | Note: {self.note_id} | Text: {self.text}"

    class Meta:
        ordering = ["-created_at"]


class NoteReaction(AuditModel):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class ReactionType(models.TextChoices):
        LIKE = "LIKE"
        DISLIKE = "DISLIKE"

    reaction = models.CharField(max_length=32, choices=ReactionType.choices)  # noqa

    class Meta:
        unique_together = ["user", "note"]
