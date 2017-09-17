from django.contrib import admin

from conman.routes.admin import RouteChildAdmin

from .models import Page


@admin.register(Page)
class PageAdmin(RouteChildAdmin):
    """
    Register `Page` in the admin.

    It's important to subclass RouteChildAdmin so that it's associated with the
    base `Route` class.
    """
