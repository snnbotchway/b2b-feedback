"""Feedback app url configuration."""
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, QuestionnaireViewSet, ResponseViewSet

router = DefaultRouter()
router.register("clients", ClientViewSet)
router.register("questionnaires", QuestionnaireViewSet)
router.register("responses", ResponseViewSet)

app_name = "feedback"

urlpatterns = router.urls
