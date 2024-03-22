from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from . import models
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from typing import Any
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    context = {
        'movie_categories_count': models.MovieCategory.objects.count(),
        'movies_count': models.Movie.objects.count(),
        'studios_count': models.Studio.objects.count(),
        'users_count': models.get_user_model().objects.count(),
    }
    return render(request, 'movies/index.html', context)

def movie_list(request: HttpRequest) -> HttpResponse:
    queryset = models.Movie.objects
    owner_username = request.GET.get('owner')
    if owner_username:
        owner = get_object_or_404(get_user_model(), username=owner_username)
        queryset = queryset.filter(owner=owner)
        movie_categories = models.MovieCategory.objects.filter(owner=owner)
    elif request.user.is_authenticated:
        movie_categories = models.MovieCategory.objects.filter(owner=request.user)
    else:
        movie_categories = models.MovieCategory.objects
    movie_category_pk = request.GET.get('movie_category_pk')
    if movie_category_pk:
        movie_category = get_object_or_404(models.MovieCategory, pk=movie_category_pk)
        queryset = queryset.filter(category=movie_category)
    search_name = request.GET.get('search_name')
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    context = {
        'movie_list': queryset.all(),
        'movie_category_list': movie_categories.all(),
        'user_list': get_user_model().objects.all().order_by('username'),
    }
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request: HttpRequest, pk:int) -> HttpResponse:
    return render(request, 'movies/movie_detail.html', {
        'movie': get_object_or_404(models.Movie, pk=pk)
    })

class MovieCategoryListView(generic.ListView):
    model = models.MovieCategory
    template_name = 'movies/movie_category_list.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.GET.get('owner'):
            queryset = queryset.filter(owner__username=self.request.GET.get('owner'))
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_list'] = get_user_model().objects.all().order_by('username')
        context['movie_category_list'] = models.MovieCategory.objects.all().filter(owner__username=self.request.GET.get('owner')) 
        return context 

def movie_category_detail(request: HttpRequest, pk:int) -> HttpResponse:
    return render(request, 'movies/movie_category_detail.html', {
        'movie_category_detail': get_object_or_404(models.MovieCategory, pk=pk)

    })

class MovieCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.MovieCategory
    template_name = 'movies/movie_category_create.html'
    fields = ('name', )

    def get_success_url(self) -> str:
        messages.success(self.request, _('movie category created successfully').capitalize())
        return reverse('movie_category_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class MovieCategoryUpdateView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.UpdateView
    ):
    model = models.MovieCategory
    template_name = 'movies/movie_category_update.html'
    fields = ('name', )

    def get_success_url(self) -> str:
        messages.success(self.request, _('movie category updated successfully').capitalize())
        return reverse('movie_category_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user

@login_required
def movie_category_delete(request: HttpRequest, pk: int) -> HttpResponse:
    movie_category = get_object_or_404(models.MovieCategory, pk=pk, owner=request.user)
    if request.method == "POST":
        movie_category.delete()
        messages.success(request, _("movie category deleted successfully"))
        return redirect('movie_category_list')
    return render(request, 'movies/movie_category_delete.html', {'movie_category': movie_category, 'object': movie_category})

