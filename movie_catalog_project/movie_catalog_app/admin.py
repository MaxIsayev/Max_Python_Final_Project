from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


# Register your models here.
admin.site.register(models.MovieCategory )
admin.site.register(models.Studio )
admin.site.register(models.Movie )
admin.site.register(models.MovieLike )
admin.site.register(models.StudioLike )