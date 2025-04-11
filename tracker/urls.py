from rest_framework.routers import DefaultRouter

from tracker.apps import TrackerConfig
from tracker.views import HabitViewSet, NiceHabitViewSet

app_name = TrackerConfig.name

router = DefaultRouter()

router.register(r"habits", HabitViewSet, basename="habits")
router.register(r"n_habits", NiceHabitViewSet, basename="n_habits")
urlpatterns = router.urls
