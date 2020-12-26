from django.urls import path
from news_videogame import views

urlpatterns = [
    path('scrap/', views.scrap_news),
]

