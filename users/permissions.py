from rest_framework import permissions
from rest_framework.permissions import BasePermission

from tracker.models import Habit, Nice_Habit


class IsOwner(BasePermission):
    """
    Разрешение, которое позволяет только владельцу редактировать или удалять объект.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ на чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, есть ли у объекта атрибут owner и является ли текущий пользователь владельцем
        return hasattr(obj, "owner") and obj.owner == request.user
