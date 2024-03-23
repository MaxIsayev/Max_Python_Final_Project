from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from tinymce.models import HTMLField

# Create your models here.
# Basic features -----------------------------------------------------
class MovieCategory(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("owner"), 
        on_delete=models.CASCADE,
        related_name='movie_categories',
    )
    description = HTMLField(_("description"), max_length=10000, null=True, blank=True)   

    class Meta:
        verbose_name = _("movie category")
        verbose_name_plural = _("movie categories")
        ordering = ['name']

    def __str__(self):
        return self.name    
    
    def get_absolute_url(self):
        return reverse("movie_category_detail", kwargs={"pk": self.pk})


class Studio(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = HTMLField(max_length=10000, null=True, blank=True)
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("owner"), 
        on_delete=models.CASCADE,
        related_name='studios'
    )
    city = models.CharField(_("city"), max_length=100, blank=True)
    country = models.CharField(_("country"), max_length=100, blank=True)
    year_start = models.IntegerField(_("year start"), blank=True)
    year_end = models.IntegerField(_("year end"), blank=True)
    founder  = models.CharField(_("founder"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("studio")
        verbose_name_plural = _("studios")
        ordering = ['name', 'year_start', 'year_end']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("studio_detail", kwargs={"pk": self.pk})
    
    @property
    def likes_by_type(self):
        return self.likes.values('like_type').annotate(count=models.Count('user'))
    

class Movie(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = HTMLField(_("description"), max_length=10000, null=True, blank=True)
    category = models.ForeignKey(
        MovieCategory,
        verbose_name=_("category"), 
        on_delete=models.CASCADE,
        related_name='movies',
    )
    studio = models.ForeignKey(
        Studio,
        verbose_name=_("studio"), 
        on_delete=models.CASCADE,
        related_name='movies',
    )
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("owner"), 
        on_delete=models.CASCADE,
        related_name='movies'
    )
    length = models.TimeField(_("length"), blank=True)
    movie_year = models.IntegerField(_("movie year"), blank=True)
    genre = models.CharField(_("genre"), max_length=100, blank=True)
    director = models.CharField(_("director"), max_length=200, blank=True)
    video_file = models.FileField(_("video file"), upload_to='video/', blank=True, null=True)
    video_image = models.ImageField(_("video picture"), upload_to='video_img/', blank=True, null=True)
    youtube_video_hash = models.CharField(
        _("YouTube video hash"), 
        max_length=50, 
        null=True, blank=True,
        help_text=_("from Youtube's video URL copy the part after 'https://www.youtube.com/watch?v='.")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("movie")
        verbose_name_plural = _("movies")
        ordering = ['name']

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"pk": self.pk})

    @property
    def likes_by_type(self):
        return self.likes.values('like_type').annotate(count=models.Count('user'))
    
# Other features ------------------------------------------------------
LIKE_TYPE_CHOICES = (
    (0, '&#x2764;&#xfe0f;'),
    (1, '&#128163;'),
    (2, '&#128293;'),
    (3, '&#128077;'),
    (4, '&#128405;'),
    (5, '&#128078;'),
)

class MovieLike(models.Model):
    movie = models.ForeignKey(
        Movie, 
        verbose_name=_("movie"), 
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='movie_likes',
    )
    like_type = models.IntegerField(_("type"), choices=LIKE_TYPE_CHOICES, default=3)

    class Meta:
        verbose_name = _("movie like")
        verbose_name_plural = _("movie likes")

    def __str__(self):
        return f"{self.movie} {self.user}"

    def get_absolute_url(self):
        return reverse("movie_like_detail", kwargs={"pk": self.pk})
    
class StudioLike(models.Model):
    studio = models.ForeignKey(
        Studio, 
        verbose_name=_("studio"), 
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='studio_likes',
    )
    like_type = models.IntegerField(_("type"), choices=LIKE_TYPE_CHOICES, default=3)

    class Meta:
        verbose_name = _("studio like")
        verbose_name_plural = _("studio likes")

    def __str__(self):
        return f"{self.studio} {self.user}"

    def get_absolute_url(self):
        return reverse("studio_like_detail", kwargs={"pk": self.pk})