from django.urls import path
from application import views

urlpatterns = [
    path('', views.inicio),
    path('registro/', views.registro)
]

