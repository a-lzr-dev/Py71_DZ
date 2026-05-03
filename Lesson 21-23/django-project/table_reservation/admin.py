from django.contrib import admin
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin

from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(ModelAdmin):
    list_display = ('id', 'number', 'seats')
#    search_fields = ('table', 'seats')
#    readonly_fields = ['current_image']
    list_filter = ['seats']
    fieldsets = [
        (
            None,
            {'fields': ('number', 'current_image', 'image', 'seats')},
        )
    ]

@admin.register(Reservation)
class ReservationAdmin(ModelAdmin):
    list_display = ('id', 'table', 'date', 'hour_start', 'hour_end', 'user', 'created_at', )
#    search_fields = ('date')
    list_filter = ['user', 'created_at']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']
    fieldsets = [
        (
            None,
            {'fields': ('table', 'date', 'hour_start', 'hour_end', 'user', 'created_at')},
        )
    ]

@admin.display(description="Текущая картинка")
def current_image(obj: Table) -> str:
    if not obj.image:
        return "-"
    return mark_safe(f'<img src="{obj.image.url}" height="200"/>')

