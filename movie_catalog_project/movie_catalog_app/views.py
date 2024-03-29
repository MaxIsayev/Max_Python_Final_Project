from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from . import models, forms
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from typing import Any
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from urllib import parse
# Create your views here.

User = get_user_model()

def index(request: HttpRequest) -> HttpResponse:
    movies = models.Movie.objects
    common_catalog = [
        (_('users').title(), User.objects.count()),
        (
            _('movie categories').title(), 
            models.MovieCategory.objects.count(), 
            reverse('movie_category_list'),
        ),
        (
            _('studios').title(), 
            models.Studio.objects.count(), 
            reverse('studio_list'),
        ),
        (
            _('movies').title(), 
            movies.count(), 
            reverse('movie_list'),
        ),       
    ]
    if request.user.is_authenticated:
        user_movies = movies.filter(owner=request.user)       
        user_catalog = [
            (
                _('movie categories').title(), 
                models.MovieCategory.objects.filter(owner=request.user).count(), 
                reverse('movie_category_list') + f"?owner={request.user.username}",
            ),
            (
                _('movies').title(), 
                user_movies.count(),
                reverse('movie_list') + f"?owner={request.user.username}",
            ),           
        ]        
    else:
        user_catalog = None        
    context = {
        'common_catalog': common_catalog,
        'user_catalog': user_catalog,       
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
    page_obj = Paginator(queryset.all(), 5).get_page(request.GET.get('page', 1))
    gets = request.GET.copy()
    if "page" in gets:
        gets.pop("page")
    filters = "&".join([f"{key}={parse.quote(value)}" for key, value in gets.items()])    
    context = {
        'movie_list': page_obj,
        'movie_category_list': movie_categories.all(),
        'user_list': get_user_model().objects.all().order_by('username'),
        'filters': filters,
        'page_obj': page_obj,
    }
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request: HttpRequest, pk:int) -> HttpResponse:
    return render(request, 'movies/movie_detail.html', {
        'movie': get_object_or_404(models.Movie, pk=pk),
        'like_types': models.LIKE_TYPE_CHOICES,
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
        'movie_category_detail': get_object_or_404(models.MovieCategory, pk=pk),        
    })

class MovieCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.MovieCategory
    template_name = 'movies/movie_category_create.html'
    fields = ('name', 'description', )

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
    fields = ('name', 'description', )

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

@login_required
def movie_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.MovieForm(request.POST, request.FILES)        
        if form.is_valid():            
            form.instance.owner = request.user
            form.save()
            messages.success(request, _("movie created successfully").capitalize())
            return redirect('movie_list')
    else:
        form = forms.MovieForm 
    return render(request, 'movies/movie_create.html', {'form': form})

@login_required
def movie_update(request: HttpRequest, pk: int) -> HttpResponse:
    movie = get_object_or_404(models.Movie, pk=pk, owner=request.user)
    if request.method == "POST":
        form = forms.MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, _("movie edited successfully"))
            return redirect('movie_detail', pk=pk)
    else:
        form = forms.MovieForm(instance=movie)    
    return render(request, 'movies/movie_update.html', {'form': form})

@login_required
def movie_delete(request: HttpRequest, pk: int) -> HttpResponse:
    movie = get_object_or_404(models.Movie, pk=pk, owner=request.user)
    if request.method == "POST":
        movie.delete()
        messages.success(request, _("movie deleted successfully"))
        return redirect('movie_list')
    return render(request, 'movies/movie_delete.html', {'movie': movie, 'object': movie})

@login_required
def movie_like(request: HttpRequest, pk: int) -> HttpResponse:
    movie = get_object_or_404(models.Movie, pk=pk)
    like_type = request.GET.get('like_type') or 3
    like = models.MovieLike.objects.filter(movie=movie, user=request.user, like_type=like_type).first()
    if not like:
         models.MovieLike.objects.create(movie=movie, user=request.user, like_type=like_type)
    else:
        like.delete()
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect('movie_list')

def studio_list(request: HttpRequest) -> HttpResponse:
    queryset = models.Studio.objects
    owner_username = request.GET.get('owner')
    if owner_username:
        owner = get_object_or_404(get_user_model(), username=owner_username)
        queryset = queryset.filter(owner=owner)          
    
    search_name = request.GET.get('search_name')
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    page_obj = Paginator(queryset.all(), 5).get_page(request.GET.get('page', 1))
    gets = request.GET.copy()
    if "page" in gets:
        gets.pop("page")
    filters = "&".join([f"{key}={parse.quote(value)}" for key, value in gets.items()])    
    context = {
        'studio_list': page_obj,        
        'user_list': get_user_model().objects.all().order_by('username'),
        'filters': filters,
        'page_obj': page_obj,
    }
    return render(request, 'movies/studio_list.html', context)

def studio_detail(request: HttpRequest, pk:int) -> HttpResponse:
    return render(request, 'movies/studio_detail.html', {
        'studio': get_object_or_404(models.Studio, pk=pk),
        'like_types': models.LIKE_TYPE_CHOICES,
    })

@login_required
def studio_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.StudioForm(request.POST)        
        if form.is_valid():            
            form.instance.owner = request.user
            form.save()
            messages.success(request, _("studio created successfully").capitalize())
            return redirect('studio_list')
    else:
        form = forms.StudioForm 
    return render(request, 'movies/studio_create.html', {'form': form})

@login_required
def studio_update(request: HttpRequest, pk: int) -> HttpResponse:
    studio = get_object_or_404(models.Studio, pk=pk, owner=request.user)
    if request.method == "POST":
        form = forms.StudioForm(request.POST, request.FILES, instance=studio)
        if form.is_valid():
            form.save()
            messages.success(request, _("studio edited successfully"))
            return redirect('studio_detail', pk=pk)
    else:
        form = forms.StudioForm(instance=studio)    
    return render(request, 'movies/studio_update.html', {'form': form})

@login_required
def studio_delete(request: HttpRequest, pk: int) -> HttpResponse:
    studio = get_object_or_404(models.Studio, pk=pk, owner=request.user)
    if request.method == "POST":
        studio.delete()
        messages.success(request, _("studio deleted successfully"))
        return redirect('studio_list')
    return render(request, 'movies/studio_delete.html', {'studio': studio, 'object': studio})

@login_required
def studio_like(request: HttpRequest, pk: int) -> HttpResponse:
    studio = get_object_or_404(models.Studio, pk=pk)
    like_type = request.GET.get('like_type') or 3
    like = models.StudioLike.objects.filter(studio=studio, user=request.user, like_type=like_type).first()
    if not like:
         models.StudioLike.objects.create(studio=studio, user=request.user, like_type=like_type)
    else:
        like.delete()
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect('studio_list')
