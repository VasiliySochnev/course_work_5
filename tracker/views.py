from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from tracker.serializers import HabitSerializer, NiceHabitSerializer
from users.permissions import IsOwner

from .models import Habit, Nice_Habit
from .paginators import HabitPaginator, NiceHabitPaginator


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    pagination_class = HabitPaginator

    def get_permissions(self, permission_classes=None):
        if self.action in ("destroy", "update", "retrieve",):
            permission_classes = [IsOwner]
        elif self.action in ("create",):
            permission_classes = [IsAuthenticated]
        elif self.action in ("list",):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)  # Проверка разрешений для объекта
        return obj

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


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
    queryset = Nice_Habit.objects.all()
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
