from django.db import models

from conman.routes.models import Route


class Page(Route):
    """A route that renders raw HTML."""
    raw_html = models.TextField(verbose_name='Raw HTML')
    template_name = 'example/page.html'
