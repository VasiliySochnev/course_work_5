from django.db import models
from django.conf import settings
from datetime import time, timezone


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
    time = models.TimeField(default=time(0, 0), verbose_name="Время выполнения привычки")
    action = models.CharField(max_length=150, verbose_name="Действие")
    related_habit = models.ForeignKey(
        'Nice_Habit',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Связанная приятная привычка",
        related_name="related_habits"
    )
    period = models.IntegerField(default=1, blank=True, null=True, verbose_name="Период выполнения (в днях)")
    reward = models.CharField(max_length=200, blank=True, null=True, verbose_name="Вознаграждение за выполнение")
    execution_time = models.TimeField(default=(0, 2), verbose_name="Время на выполнение привычки")
    is_public = models.BooleanField(default=True, verbose_name="Признак публичности")
    last_performed = models.DateField(null=True, blank=True, editable=False, verbose_name="Поле для хранения даты последнего выполнения")

    def perform_habit(self):
        """Метод для сохранения даты выполнения привычки."""

        self.last_performed = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.action} в {self.time} {self.place} ({'Публичная' if self.is_public else 'Приватная'})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['action']



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
    is_nice = models.BooleanField(default=True, verbose_name="Признак приятной привычки")

    def __str__(self):
        return f"{self.action} ({'Публичная' if self.is_public else 'Приватная'})"

    class Meta:
        verbose_name = "Приятная привычка"
        verbose_name_plural = "Приятные привычки"
        ordering = ['action']



