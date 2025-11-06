from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('triage-reports/', views.triage_reports, name='triage_reports'),
    path('clinic-info/', views.clinic_info, name='clinic_info'),
]

