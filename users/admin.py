from django import forms
from django.contrib import admin
from django.forms.widgets import TimeInput

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


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = "__all__"
        widgets = {
            "time": TimeInput(format="%H:%M"),  # Устанавливаем формат времени
        }


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    form = HabitForm
    list_display = (
        "owner",
        "place",
        "time",
        "days_of_week",
        "period",
        "action",
        "execution_time",
        "related_habit",
        "reward",
        "is_public",
        "id",
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
        "id",
    )
    search_fields = ("action",)
    list_filter = ("owner",)
