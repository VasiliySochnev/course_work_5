from datetime import time

from django.conf import settings
from django.db import models
from django.utils import timezone


class Nice_Habit(models.Model):
    """Модель приятной привычки."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель приятной привычки",
        blank=True,
        null=True,
    )
    action = models.CharField(max_length=150, verbose_name="Действие приятной привычки")
    is_public = models.BooleanField(default=True, verbose_name="Признак публичности")
    is_nice = models.BooleanField(
        default=True, verbose_name="Признак приятной привычки"
    )
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.action}"

    class Meta:
        verbose_name = "Приятная привычка"
        verbose_name_plural = "Приятные привычки"
        ordering = ["action"]


class Habit(models.Model):
    """Модель полезной привычки."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        blank=True,
        null=True,
    )
    place = models.CharField(max_length=150, verbose_name="Место выполнения привычки")
    time = models.TimeField(
        default=time(0, 0, 0),
        verbose_name="Время выполнения привычки",
        help_text="00:00:00",
    )
    action = models.CharField(max_length=150, verbose_name="Действие")
    related_habit = models.ForeignKey(
        Nice_Habit,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Связанная приятная привычка",
        related_name="related_habits",
    )
    reward = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Вознаграждение за выполнение",
    )
    execution_time = models.DurationField(
        default=timezone.timedelta(minutes=2),
        verbose_name="Время на выполнение привычки",
        help_text="00:00:00",
    )
    is_public = models.BooleanField(default=True, verbose_name="Признак публичности")

    days_of_week = models.CharField(
        max_length=100,
        default="пн, вт, ср, чт, пт, сб, вс",
        verbose_name="Дни недели",
        help_text="Введите дни недели через запятую (например, 'пн, вт, ср'), по умолчанию: ежедневно",
    )
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.action} в {self.time} {self.place} ({'Публичная' if self.is_public else 'Приватная'})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["action"]
