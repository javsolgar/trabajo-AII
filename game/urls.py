from django.urls import path
from game import views

urlpatterns = [
    path('scrap_games/', views.scrap_games),
]

