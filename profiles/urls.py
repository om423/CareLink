from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('create/', views.create_profile, name='create'),
    path('edit/', views.edit_profile, name='edit'),
]

