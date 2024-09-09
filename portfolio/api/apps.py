from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class APIConfig(AppConfig):
    name = "portfolio.api"
    verbose_name = _("API")
