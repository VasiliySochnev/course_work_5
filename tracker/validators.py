from django.utils import timezone
from rest_framework import serializers

from tracker.models import Nice_Habit


class TimeValidator:
    """Валидация для времени выполнения."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_time = dict(value).get(self.field)
        if tmp_time and tmp_time > timezone.timedelta(minutes=2):
            raise serializers.ValidationError(
                "Время на выполнение не должно превышать 2 минут."
            )


class RewardValidator:
    """Валидация для полей related_habit и reward."""

    def __init__(self, related_habit_field, reward_field):
        self.related_habit_field = related_habit_field
        self.reward_field = reward_field

    def __call__(self, value):
        related_habit = value.get(self.related_habit_field)
        reward = value.get(self.reward_field)
        if (related_habit is not None and reward) or (reward is None and related_habit):
            raise serializers.ValidationError(
                'Можно заполнить только одно из полей: "Связанная приятная привычка" или "Вознаграждение".'
            )


class RelatedHabitValidator:
    """Валидация для поля related_habit."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        nice_habit_id = value.get(self.field)

        # Проверяем, существует ли привычка с данным ID
        if nice_habit_id is not None:
            try:
                nice_habit = Nice_Habit.objects.get(id=nice_habit_id)
                if not nice_habit.is_nice:
                    raise serializers.ValidationError(
                        "В связанные привычки могут попадать только привычки с признаком приятной привычки."
                    )
            except Nice_Habit.DoesNotExist:
                raise serializers.ValidationError("Привычка с указанным ID не найдена.")


class Days_Of_WeekValidator:
    """Валидация для поля days_of_week."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        days_of_week = value.get(self.field)
        print(self.field, value)
        if days_of_week is None:
            raise serializers.ValidationError(
                "Привычка не может выполняться реже, чем 1 раз в 7 дней, "
                "введите дни(день) недели через запятую (например, 'пн, вт, ср')"
            )
