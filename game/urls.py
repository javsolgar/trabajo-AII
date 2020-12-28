from django.urls import path
from game import views

urlpatterns = [
    path('scrap_games/', views.scrap_games),
    path('games/', views.list_games),
    path('games/<game_title>', views.show_game)
]

