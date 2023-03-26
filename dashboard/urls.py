from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.index, name='dashboard'),
    path('forget/', views.forget, name='forget'),
    path('change_password/', views.change_password, name='change_password'),
]