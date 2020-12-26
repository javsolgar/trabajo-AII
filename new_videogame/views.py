from django.shortcuts import render
from new_videogame import scrap_news


def scrap_news(request):
    #scrap_news.download_news()
    return render(request, 'scrap_news.html')
