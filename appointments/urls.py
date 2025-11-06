from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book_appointment, name='book'),
    path('<int:pk>/', views.detail, name='detail'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
]

