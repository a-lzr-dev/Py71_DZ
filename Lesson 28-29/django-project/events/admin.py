from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Event

@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('id', 'name', 'meeting_time', 'description')
    list_filter = ['meeting_time']
    fieldsets = [
        (
            None,
            {'fields': ('name', 'meeting_time', 'description')},
        )
    ]