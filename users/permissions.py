from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission


#
#
# class Is_Staff(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.groups.filter(name="Модераторы").exists():
#             return True
#
#         return False


class Is_Users(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Пользователи").exists():
            return True

        return False


# class Is_Owner(BasePermission):
#     def has_permission(self, request, view):
#
#         lesson = get_object_or_404(Lesson, pk=view.kwargs["pk"])
#         if lesson.owner == request.user:
#
#             return True
#         return False
