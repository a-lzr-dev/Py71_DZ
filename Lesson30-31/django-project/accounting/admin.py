from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django_celery_beat.admin import (
    ClockedScheduleAdmin,
    CrontabScheduleAdmin,
    IntervalScheduleAdmin,
    PeriodicTaskAdmin,
    SolarScheduleAdmin,
)
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm

from .models import User

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


admin.site.unregister(PeriodicTask)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(IntervalSchedule)


@admin.register(PeriodicTask)
class UnfoldPeriodicTaskAdmin(PeriodicTaskAdmin, ModelAdmin):
    pass


@admin.register(ClockedSchedule)
class UnfoldClockedScheduleAdmin(ClockedScheduleAdmin, ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class UnfoldCrontabScheduleAdmin(CrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule)
class UnfoldSolarScheduleAdmin(SolarScheduleAdmin, ModelAdmin):
    pass


@admin.register(IntervalSchedule)
class UnfoldIntervalScheduleAdmin(IntervalScheduleAdmin, ModelAdmin):
    pass
