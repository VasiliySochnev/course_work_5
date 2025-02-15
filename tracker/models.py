from django.db import models
from datetime import time

from rest_framework.exceptions import ValidationError


from config import settings


class Habit(models.Model):
    """Модель привычки."""

    title = models.CharField(max_length=150, verbose_name="Название привычки")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        blank=True,
        null=True,
    )
    place = models.CharField(max_length=150, verbose_name="Место выполнения привычки")
    time = models.TimeField(
        default=time(0, 0), verbose_name="Время, когда необходимо выполнять привычку"
    )
    action = models.CharField(max_length=150, verbose_name="Действие")
    is_nice_habit = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        related_name="related_habits",
    )
    period = models.IntegerField(
        default=1, blank=True, null=True, verbose_name="Период выполнения (в днях)"
    )
    reward = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Вознаграждение за выполнение",
    )
    execution_time = models.TimeField(
        default=(0, 2), verbose_name="Время выполнения привычки"
    )
    is_public = models.BooleanField(default=True, verbose_name="Признак публичности")

    def __str__(self):
        return f"{self.title} ({'Публичная' if self.is_public else 'Приватная'})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['title']

    def clean(self):
        if self.period is not None and self.period <= 0:
            raise ValidationError('Период выполнения должен быть положительным числом.')


