"""
Django admin integration for Routes.

Because Route is based on django-polymorphic, their documentation
should really help in understanding the code here:

https://django-polymorphic.readthedocs.io/en/stable/admin.html
"""

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicParentModelAdmin,
)

from .models import Route


class RouteChildAdmin(PolymorphicChildModelAdmin):
    """
    Base admin class for all Route subclasses.

    Every subclass of Route that needs to be represented in the admin would
    benefit from using a ModelAdmin that is a subclass of this. eg:

        @django.contrib.admin.register(CustomRoute)
        class CustomRouteAdmin(RouteChildAdmin):
            pass
    """
    base_fields = ('url',)
    base_model = Route


@admin.register(Route)
class RouteParentAdmin(PolymorphicParentModelAdmin):
    """ModelAdmin for the base Route model."""
    base_model = Route
    list_display = (
        'url',
        'polymorphic_ctype',
    )
    list_filter = (
        ('polymorphic_ctype', admin.RelatedOnlyFieldListFilter),
    )
    ordering = ('url',)
    search_fields = ('url',)

    def get_child_models(self):
        """Return every admin-registered subclass of Route."""
        paths = settings.CONMAN_ADMIN_ROUTES
        return [apps.get_model(model_path) for model_path in paths]
