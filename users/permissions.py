from rest_framework.permissions import BasePermission

from tracker.models import Habit, Nice_Habit


class IsPublic(BasePermission):
    def has_permission(self, request, view):

        if hasattr(request, "habit") and request.habit.is_public:
            return True
        if hasattr(request, "nace_habit") and request.nace_habit.is_public:
            return True

        return False


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        # Получаем queryset в зависимости от типа привычки
        if view.request.query_params.get("type") == "nice":
            queryset = Nice_Habit.objects.filter(owner=request.user)
        else:
            queryset = Habit.objects.filter(owner=request.user)

        # Проверяем, есть ли у пользователя доступ к хотя бы одному объекту
        return queryset.exists()


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Модераторы").exists():
            return True

        return False
