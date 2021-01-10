from django.urls import path
from recommendation import views

urlpatterns = [
    path('list_juego_recommendation/', views.list_games)

]

