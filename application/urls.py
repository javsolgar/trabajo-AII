from django.urls import path
from application import views

urlpatterns = [
    path('', views.inicio),
    path('registro/', views.registro),
    path('scrap_all/', views.scrap_all)
]

