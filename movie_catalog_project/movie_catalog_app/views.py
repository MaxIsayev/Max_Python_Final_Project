from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from . import models
# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    context = {
        'movie_categorys_count': models.MovieCategory.objects.count(),
        'movies_count': models.Movie.objects.count(),
        'studios_count': models.Studio.objects.count(),
        'users_count': models.get_user_model().objects.count(),
    }
    return render(request, 'movies/index.html', context)