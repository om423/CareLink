from django.urls import path

from . import views

app_name = "doctors"

urlpatterns = [
    path("", views.index, name="index"),
    path("find/", views.find_doctor, name="find_doctor"),
    path("assign/<int:interaction_id>/", views.assign_to_self, name="assign_to_self"),
    path("notes/<int:interaction_id>/add/", views.add_note, name="add_note"),
    path("feed/", views.triage_feed, name="triage_feed"),
    path("triage/<int:interaction_id>/pdf/", views.triage_pdf, name="triage_pdf"),
]
