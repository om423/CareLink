from django.urls import path
from . import views

app_name = "doctors"

urlpatterns = [
    path("", views.index, name="index"),
]
