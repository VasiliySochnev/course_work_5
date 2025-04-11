from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tracker.serializers import (
    HabitSerializer,
    HabitUpdateSerializer,
    NiceHabitSerializer,
)
from users.permissions import IsOwner

from .models import Habit, Nice_Habit
from .paginators import HabitPaginator, NiceHabitPaginator


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для модели привычка."""

    queryset = Habit.objects.filter(is_public=True)
    pagination_class = HabitPaginator

    def get_serializer_class(self):
        """Метод для получения сериализатора в зависимости от действия."""
        if self.action in (
            "create",
            "destroy",
            "retrieve",
            "list",
        ):
            return HabitSerializer
        elif self.action == "update" or self.action == "partial_update":
            return HabitUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        """Метод для распределения ограничений в зависимости от действия."""
        if self.action in (
            "destroy",
            "update",
            "partial_update",
            "retrieve",
        ):
            permission_classes = [IsOwner]
        elif self.action in ("create",):
            permission_classes = [IsAuthenticated]
        elif self.action in ("list",):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Метод для создания привычки с валидацией дней."""
        days_of_week = serializer.validated_data.get("days_of_week", "")
        if days_of_week:
            days = [day.strip().lower() for day in days_of_week.split(",")]
            unique_days = sorted(set(days))
            formatted_days = ", ".join(unique_days)
            serializer.save(days_of_week=formatted_days)
        else:
            serializer.save()

        # сохраненной привычке присваиваем владельца
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()

    def update(self, request, *args, **kwargs):
        """Метод для редактирования привычки с валидацией дней"""
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        days_of_week = serializer.validated_data.get("days_of_week", None)
        valid_days = {"пн", "вт", "ср", "чт", "пт", "сб", "вс"}

        if days_of_week is not None:
            # Разделяем и нормализуем дни
            days = [day.strip().lower() for day in days_of_week.split(",")]

            # Фильтруем только допустимые дни
            unique_days = sorted(set(day for day in days if day in valid_days))

            if unique_days:
                formatted_days = ", ".join(unique_days)
                instance.days_of_week = formatted_days
            else:
                return Response(
                    {"error": "Не введено ни одного допустимого дня недели."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Обновляем остальные поля, если они есть
        for attr, value in serializer.validated_data.items():
            if attr != "days_of_week":
                setattr(instance, attr, value)

        # Сохраняем обновленный экземпляр
        instance.save()
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="own_habits")
    def own_habits(self, request):
        # метод для вывода списка привычек владельца
        own_habits = Habit.objects.filter(owner=request.user)
        serializer = HabitSerializer(own_habits, many=True)
        return Response(serializer.data)


class NiceHabitViewSet(viewsets.ModelViewSet):
    """ViewSet для модели приятная привычка."""

    serializer_class = NiceHabitSerializer
    queryset = Nice_Habit.objects.filter(is_public=True)
    pagination_class = NiceHabitPaginator

    def get_permissions(self):
        """Метод для распределения ограничений в зависимости от действия."""
        if self.action in (
            "destroy",
            "update",
            "partial_update",
            "retrieve",
        ):
            permission_classes = [IsOwner]
        elif self.action in ("create",):
            permission_classes = [IsAuthenticated]
        elif self.action in ("list",):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_nice_habit = serializer.save()
        new_nice_habit.owner = self.request.user
        new_nice_habit.save()

    @action(detail=False, methods=["get"], url_path="own_n_habits")
    def own_n_habits(self, request):
        # метод для вывода списка приятных привычек владельца
        own_n_habits = Nice_Habit.objects.filter(owner=request.user)
        serializer = self.get_serializer(own_n_habits, many=True)
        return Response(serializer.data)
