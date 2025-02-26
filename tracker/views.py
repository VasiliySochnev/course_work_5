from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tracker.serializers import HabitSerializer, NiceHabitSerializer
from users.permissions import IsOwner

from .models import Habit, Nice_Habit
from .paginators import HabitPaginator, NiceHabitPaginator
from .tasks import message_of_habit


class HabitViewSet(viewsets.ModelViewSet):
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
        days_of_week = serializer.validated_data.get("days_of_week", "")
        if days_of_week:
            days = [day.strip().lower() for day in days_of_week.split(",")]
            unique_days = sorted(set(days))
            formatted_days = ", ".join(unique_days)
            serializer.save(days_of_week=formatted_days)
        else:
            serializer.save()

        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()

    def update(self, request, *args, **kwargs):
        # Используем встроенный метод для получения объекта
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
                return Response({"error": "Не введено ни одного допустимого дня недели."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Обновляем остальные поля, если они есть
        for attr, value in serializer.validated_data.items():
            if attr != "days_of_week":
                setattr(instance, attr, value)

        # Сохраняем обновленный экземпляр
        instance.save()
        return Response(serializer.data)


class NiceHabitListView(generics.ListAPIView):
    serializer_class = NiceHabitSerializer
    queryset = Nice_Habit.objects.filter(is_public=True)
    pagination_class = NiceHabitPaginator
    permission_classes = [IsAuthenticated]


class NiceHabitCreateView(generics.CreateAPIView):
    serializer_class = NiceHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_nice_habit = serializer.save()
        new_nice_habit.owner = self.request.user
        new_nice_habit.save()


class NiceHabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = NiceHabitSerializer
    queryset = Nice_Habit.objects.filter()
    permission_classes = [IsOwner]


class NiceHabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = NiceHabitSerializer
    queryset = Nice_Habit.objects.all()
    permission_classes = [IsOwner]


class NiceHabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Nice_Habit.objects.all()
    permission_classes = [IsOwner]


class HabitOwnerListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [IsOwner]


class NiceHabitOwnerListView(generics.ListAPIView):
    serializer_class = NiceHabitSerializer
    queryset = Nice_Habit.objects.all()
    pagination_class = NiceHabitPaginator
    permission_classes = [IsOwner]
