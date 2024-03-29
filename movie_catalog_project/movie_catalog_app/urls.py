from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'), 
    path('movie_categories/', views.MovieCategoryListView.as_view() , name='movie_category_list'), 
    path('movie_category/<int:pk>/', views.movie_category_detail, name='movie_category_detail'),
    path('movie_categories/create/', views.MovieCategoryCreateView.as_view(), name='movie_category_create'),
    path('movie_category/<int:pk>/edit/', views.MovieCategoryUpdateView.as_view(), name='movie_category_update'),
    path('movie_category/<int:pk>/delete/', views.movie_category_delete, name='movie_category_delete'),
    path('user_profile/', include('user_profile.urls')),
    path('movies/create/', views.movie_create, name='movie_create'),
    path('movie/<int:pk>/edit/', views.movie_update, name='movie_update'),
    path('movie/<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    path('movie/<int:pk>/like/', views.movie_like, name='movie_like'),
    path('studios/', views.studio_list, name='studio_list'),
    path('studio/<int:pk>/', views.studio_detail, name='studio_detail'),
    path('studio/create/', views.studio_create, name='studio_create'),
    path('studio/<int:pk>/edit/', views.studio_update, name='studio_update'),
    path('studio/<int:pk>/delete/', views.studio_delete, name='studio_delete'),
    path('studio/<int:pk>/like/', views.studio_like, name='studio_like'),
]


