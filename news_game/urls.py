from django.urls import path
from news_game import views

urlpatterns = [
    path('scrap_news_games/', views.scrap_news),
    path('news/', views.list_news)
]

