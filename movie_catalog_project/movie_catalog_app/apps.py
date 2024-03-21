from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MovieCatalogAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie_catalog_app'

    class Meta:
        verbose_name = _('movie catalog app')