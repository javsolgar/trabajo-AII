from django.urls import path
from application import views

urlpatterns = [
    path('', views.inicio),
    path('registro/', views.registro),
    path('scrap_all/', views.scrap_all),
    path('cargar_juegos_bd/', views.carga_juegos_bd),
    path('load_RS/', views.carga_rs)
]

