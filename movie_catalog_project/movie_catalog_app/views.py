from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
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

def movie_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'movies/movie_list.html', {
        'movie_list': models.Movie.objects.all(),
    })

def movie_detail(request: HttpRequest, pk:int) -> HttpResponse:
    return render(request, 'movies/movie_detail.html', {
        'movie': get_object_or_404(models.Movie, pk=pk)
    })