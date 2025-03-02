from django.urls import path
from rest_framework.routers import DefaultRouter

from tracker.apps import TrackerConfig
from tracker.views import (HabitOwnerListView, HabitViewSet,
                           NiceHabitCreateView, NiceHabitDestroyAPIView,
                           NiceHabitListView, NiceHabitOwnerListView,
                           NiceHabitRetrieveAPIView, NiceHabitUpdateAPIView)

app_name = TrackerConfig.name

router = DefaultRouter()

router.register(r"habits", HabitViewSet, basename="habits")

urlpatterns = [
    path("n_habit/create/", NiceHabitCreateView.as_view(), name="n_habit-create"),
    path("n_habit/", NiceHabitListView.as_view(), name="n_habit-list"),
    path(
        "n_habit/<int:pk>/", NiceHabitRetrieveAPIView.as_view(), name="n_habit-detail"
    ),
    path(
        "n_habit/update/<int:pk>/",
        NiceHabitUpdateAPIView.as_view(),
        name="n_habit-update",
    ),
    path(
        "n_habit/delete/<int:pk>/",
        NiceHabitDestroyAPIView.as_view(),
        name="n_habit-delete",
    ),
    path("own_habit/", HabitOwnerListView.as_view(), name="own_habit-list"),
    path("own_n_habit/", NiceHabitOwnerListView.as_view(), name="own_n_habit-list"),
] + router.urls
