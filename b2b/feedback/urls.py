"""Feedback app url configuration."""
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import (
    ClientViewSet,
    MonthlyFeedbackViewSet,
    QuestionnaireViewSet,
    ResponseViewSet,
)

router = DefaultRouter()
router.register("clients", ClientViewSet)
router.register("questionnaires", QuestionnaireViewSet)
router.register("monthly-feedback", MonthlyFeedbackViewSet, basename="monthly-feedback")


questionnaires_router = NestedDefaultRouter(
    router, "questionnaires", lookup="questionnaire"
)
questionnaires_router.register(
    "responses", ResponseViewSet, basename="questionnaire-responses"
)

app_name = "feedback"

urlpatterns = router.urls + questionnaires_router.urls
