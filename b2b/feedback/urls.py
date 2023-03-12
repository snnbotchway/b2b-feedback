"""Feedback app url configuration."""
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet

router = DefaultRouter()
router.register("clients", ClientViewSet)

app_name = "feedback"

urlpatterns = router.urls
