from datetime import time, timedelta, timezone

from rest_framework.serializers import ValidationError


class TimeValidator:
    """Валидация для времени выполнения"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        execution_time = value.get(self.field)
        if execution_time > time(0, 2):
            raise ValidationError('Время на выполнение не должно превышать 2 минут.')

class RewardValidator:
    """Валидация для полей related_habit и reward."""

    def __init__(self, related_habit_field, reward_field):
        self.related_habit_field = related_habit_field
        self.reward_field = reward_field

    def __call__(self, value):
        related_habit = value.get(self.related_habit_field)
        reward = value.get(self.reward_field)
        if (related_habit is not None and reward) or (related_habit is None and not reward):
            raise ValidationError(
                'Можно заполнить только одно из полей: "Связанная приятная привычка" или "Вознаграждение".')


class RelatedHabitValidator:
    """Валидация для поля related_habit."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        nice_habit = value.get(self.field)
        if not nice_habit.object.is_nice:
            raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки.')

class PeriodValidator:
    """Валидация для поля period."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        period = value.get(self.field)
        if period is None:
            return

        if period > timedelta(days=7):
            raise ValidationError('Привычка не может выполняться реже, чем 1 раз в 7 дней.')

class ExecutionValidator:
    """Валидация для проверки выполнения привычки."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        last_performed = value.get(self.field)
        if last_performed:
            days_last_performed = (timezone.now().date() - last_performed).days
            if days_last_performed > 7:
                raise ValidationError("Нельзя не выполнять привычку более 7 дней.")
