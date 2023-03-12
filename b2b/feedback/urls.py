"""Feedback app url configuration."""
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, QuestionnaireViewSet

router = DefaultRouter()
router.register("clients", ClientViewSet)
router.register("questionnaires", QuestionnaireViewSet)

app_name = "feedback"

urlpatterns = router.urls
