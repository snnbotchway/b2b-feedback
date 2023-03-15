"""Account app urls."""
from django.urls import path

from .views import CreateUserTokenView

app_name = "account"

urlpatterns = [
    path("login/", CreateUserTokenView.as_view(), name="login"),
]
