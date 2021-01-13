from django.urls import path
from recommendation import views

urlpatterns = [
    path('list_game_recommendation/', views.list_games),
    path('game_recomendation/', views.show_game),
    path('get_my_recomendations/', views.get_ratings),
]

