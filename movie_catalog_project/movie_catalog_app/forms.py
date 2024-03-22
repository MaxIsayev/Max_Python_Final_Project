from django import forms
from . import models

class MovieForm(forms.ModelForm):
    class Meta:
        model = models.Movie
        fields = ('name', 'description', 'category', 'studio', 'length', 'movie_year', 'genre', 'director', 'video_file', 'video_image', 'youtube_video_hash',)        