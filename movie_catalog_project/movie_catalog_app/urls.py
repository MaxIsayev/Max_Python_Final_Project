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
]


