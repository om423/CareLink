from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.index, name="index"),
    path("onboarding/", views.onboarding, name="onboarding"),
    path("edit/", views.edit_profile, name="edit"),
]
