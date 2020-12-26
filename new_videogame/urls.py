from django.urls import path
from new_videogame import views

urlpatterns = [
    path('scrap/', views.scrap_news),
]

