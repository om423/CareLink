from django.urls import path
from . import views

app_name = "triage"

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/", views.chat, name="chat"),
]
