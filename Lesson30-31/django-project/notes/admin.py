from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Note, Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    pass


class TagInline(TabularInline):
    model = Note.tags.through
    extra = 1


@admin.register(Note)
class NoteAdmin(ModelAdmin):
    list_display = ["id", "title", "user", "created_at", "current_image", "tags_list"]
    search_fields = ["title", "content"]
    list_filter = ["user", "created_at"]
    date_hierarchy = "created_at"
    filter_horizontal = ["tags"]
    list_select_related = ["user"]
    readonly_fields = ["created_at", "updated_at", "current_image"]
    list_per_page = 10
    inlines = [TagInline]
    fieldsets = [
        (
            None,
            {"fields": ("title", "user", "current_image", "image", "content")},
        ),
        (
            "Даты",
            {"fields": ("created_at", "updated_at")},
        ),
    ]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    actions = ["clear_tags_action"]

    @admin.display(description="Текущая картинка")
    def current_image(self, obj: Note) -> str:
        if not obj.image:
            return "-"
        return mark_safe(f'<img src="{obj.image.url}" height="200" />')

    @admin.display(description="Теги")
    def tags_list(self, obj: Note) -> str:
        text = ""
        for tag in obj.tags.all():
            text += f"<li>{tag}</li>"
        return mark_safe(text)

    @admin.action(description="Очистить теги")
    def clear_tags_action(self, request, queryset):
        for obj in queryset:
            obj.tags.clear()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")
