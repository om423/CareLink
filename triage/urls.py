from django.urls import path

from . import views

app_name = "triage"

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/", views.chat, name="chat"),
    path("chat/api/", views.chat_api, name="chat_api"),
    path("history/", views.history, name="history"),
    path("history/<int:interaction_id>/", views.detail, name="detail"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path(
        "admin/notes/<int:interaction_id>/update/",
        views.update_doctor_notes,
        name="update_doctor_notes",
    ),
    path(
        "admin/review/<int:interaction_id>/complete/",
        views.mark_review_completed,
        name="mark_review_completed",
    ),
]
