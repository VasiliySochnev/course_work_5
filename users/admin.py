from django.contrib import admin

from tracker.models import Habit, Nice_Habit
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "avatar",
        "email",
        "first_name",
        "last_name",
        "phone",
        "city",
        "is_active",
    )
    search_fields = ("email",)
    list_filter = ("email",)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "place",
        "time",
        "action",
        "related_habit",
        "period",
        "reward",
        "execution_time",
        "is_public",
    )
    search_fields = ("action",)
    list_filter = ("owner",)


@admin.register(Nice_Habit)
class NiceHabitAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "action",
        "is_public",
        "is_nice",
    )
    search_fields = ("action",)
    list_filter = ("owner",)
