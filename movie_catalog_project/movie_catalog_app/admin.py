from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models

class MovieCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'total_movies', 'recent_movies']
    list_display_links = ['name']
    list_filter = ['owner']
    search_fields = ['name']
    autocomplete_fields = ['owner']
    fieldsets = (
        (None, {
            "fields": (
                'name', 'owner', 'description',
            ),
        }),
    )

    def total_movies(self, obj: models.MovieCategory):
        return obj.movies.count()
    total_movies.short_description = _("total movies")

    def recent_movies(self, obj: models.MovieCategory):
        return "; ".join(obj.movies.order_by('movie_year').values_list('name', flat=True)[:3])
    recent_movies.short_description = _("recent movies")
    
class StudioAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'city', 'country', 'year_start', 
                    'year_end', 'founder', 'total_movies', 'recent_movies']
    list_filter = ['owner', 'city', 'country', 'year_start', 'year_end', 
                   'founder']
    search_fields = ['name', 'description', 'owner__last_name', 
                     'owner__username', 'city', 'country', 'founder']
    list_editable = ['owner', 'city', 'country', 'founder']
    readonly_fields = ['id']
    autocomplete_fields = ['owner']
    fieldsets = (
        (_("general").title(), {
            "fields": (
                ('name', 'city', 'country'),
                'description', 'founder',
            ),
        }),
        (_("ownership").title(), {
            "fields": (
                ('owner'),
            ),
        }),
        (_("period").title(), {
            "fields": (
                ('year_start', 'year_end', 'id'),
            ),
        }),
    )
    def total_movies(self, obj: models.Studio):
        return obj.movies.count()
    total_movies.short_description = _("total movies")

    def recent_movies(self, obj: models.Studio):
        return "; ".join(obj.movies.order_by('movie_year').values_list('name', flat=True)[:3])
    recent_movies.short_description = _("recent movies")

class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'studio', 'owner', 'length', 
                    'movie_year', 'genre', 'director', 'video_file', 
                    'video_image']
    list_filter = ['category', 'studio', 'owner', 'movie_year', 'genre']
    search_fields = ['name', 'description', 'category__name', 'studio__name',
                     'owner__last_name', 'owner__username', 'genre', 
                     'director', 'movie_year']
    list_editable = ['owner', 'category', 'studio', 'genre', 'director']
    readonly_fields = ['id']
    autocomplete_fields = ['category', 'owner']
    fieldsets = (
        (_("general").title(), {
            "fields": (
                ('name', 'genre'),
                'description', 
            ),
        }),
        (_("ownership").title(), {
            "fields": (
                ('owner', 'category', 'studio', 'director'),
            ),
        }),
        (_("temporal tracking").title(), {
            "fields": (
                ('length', 'movie_year', 'id'),
            ),
        }),
        (_("files and links").title(), {
            "fields": (
                ('video_file', 'video_image', 'youtube_video_hash'),
            ),
        }),
    )

class MovieLikeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'like_type']

class StudioLikeAdmin(admin.ModelAdmin):
    list_display = ['studio', 'user', 'like_type']

# Register your models here.
admin.site.register(models.MovieCategory, MovieCategoryAdmin)
admin.site.register(models.Studio, StudioAdmin)
admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.MovieLike, MovieLikeAdmin)
admin.site.register(models.StudioLike, StudioLikeAdmin)