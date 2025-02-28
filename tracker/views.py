from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tracker.serializers import HabitSerializer, NiceHabitSerializer
from users.permissions import IsOwner

from .models import Habit, Nice_Habit
from .paginators import HabitPaginator, NiceHabitPaginator


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для модели привычка."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    pagination_class = HabitPaginator

    def get_permissions(self):
        if self.action in (
            "destroy",
            "update",
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


class NiceHabitListView(generics.ListAPIView):
    """Контроллер для вывода списка приятных привычек."""

    serializer_class = NiceHabitSerializer
    queryset = Nice_Habit.objects.filter(is_public=True)
    pagination_class = NiceHabitPaginator
    permission_classes = [IsAuthenticated]


class NiceHabitCreateView(generics.CreateAPIView):
    """Контроллер для создания приятной привычки."""

    serializer_class = NiceHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_nice_habit = serializer.save()
        new_nice_habit.owner = self.request.user
        new_nice_habit.save()


class NiceHabitRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для детального просмотра приятной привычки."""
    serializer_class = NiceHabitSerializer
    queryset = Nice_Habit.objects.filter()
    permission_classes = [IsOwner]


class NiceHabitUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для редактирования приятной привычки."""

    serializer_class = NiceHabitSerializer
    queryset = Nice_Habit.objects.all()
    permission_classes = [IsOwner]


class NiceHabitDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления приятной привычки."""
    queryset = Nice_Habit.objects.all()
    permission_classes = [IsOwner]


class HabitOwnerListView(generics.ListAPIView):
    """Контроллер для вывода списка привычек владельца."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [IsOwner]


class NiceHabitOwnerListView(generics.ListAPIView):
    """Контроллер для вывода списка приятных привычек владельца."""
    serializer_class = NiceHabitSerializer
    queryset = Nice_Habit.objects.all()
    pagination_class = NiceHabitPaginator
    permission_classes = [IsOwner]
