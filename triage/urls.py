from django.urls import path
from . import views

app_name = "triage"

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/", views.chat, name="chat"),
    path("chat/api/", views.chat_api, name="chat_api"),
    path("history/", views.history, name="history"),
    path("history/<int:interaction_id>/", views.detail, name="detail"),
]
