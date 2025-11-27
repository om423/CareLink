from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path("", views.index, name="index"),
    path("book/", views.book, name="book"),
    path("<int:appointment_id>/", views.detail, name="detail"),
    path("<int:appointment_id>/edit/", views.edit, name="edit"),
    path("<int:appointment_id>/cancel/", views.cancel, name="cancel"),
    path("doctor/", views.doctor_appointments, name="doctor_appointments"),
    path("<int:appointment_id>/confirm/", views.confirm, name="confirm"),
    path("<int:appointment_id>/complete/", views.complete, name="complete"),
]
