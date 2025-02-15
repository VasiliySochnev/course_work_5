from rest_framework import serializers
from tracker.models import Habit, Nice_Habit
from tracker.validators import TimeValidator, RewardValidator, RelatedHabitValidator, PeriodValidator, \
    ExecutionValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            TimeValidator(field="time"),
            RewardValidator(related_habit_field="related_habit", reward_field="reward"),
            RelatedHabitValidator(field="related_habit"),
            PeriodValidator(field="period"),
            ExecutionValidator(field="last_performed")
        ]


class NiceHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nice_Habit
        fields = "__all__"
