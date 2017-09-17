from django.contrib import admin

from conman.routes.admin import RouteChildAdmin

from .models import RouteRedirect, URLRedirect


@admin.register(RouteRedirect)
class RouteRedirectAdmin(RouteChildAdmin):
    """Ensure RouteRedirect is registered in the admin."""


@admin.register(URLRedirect)
class URLRedirectAdmin(RouteChildAdmin):
    """Ensure URLRedirect is registered in the admin."""
