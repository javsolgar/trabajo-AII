from django.urls import path
from recomendation import views

urlpatterns = [
    path('list_juego_recommendation/', views.list_games)

]

