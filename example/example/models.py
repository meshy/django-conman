from django.db import models

from conman.routes.models import Route

from .views import page_view


class Page(Route):
    """A route that renders raw HTML."""
    raw_html = models.TextField(verbose_name='Raw HTML')
    view = page_view
