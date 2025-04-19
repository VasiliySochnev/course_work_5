from rest_framework import serializers

from tracker.models import Habit, Nice_Habit
from tracker.validators import (Days_Of_WeekValidator, RelatedHabitValidator,
                                RewardValidator, TimeValidator)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            TimeValidator(field="execution_time"),
            RewardValidator(related_habit_field="related_habit", reward_field="reward"),
            RelatedHabitValidator(field="related_habit_id"),
            Days_Of_WeekValidator(field="days_of_week"),
        ]


class HabitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            TimeValidator(field="execution_time"),
            RewardValidator(related_habit_field="related_habit", reward_field="reward"),
            RelatedHabitValidator(field="related_habit_id"),
        ]


class NiceHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nice_Habit
        fields = "__all__"
