from django.contrib import admin
from polymorphic_tree.admin import (
    PolymorphicMPTTChildModelAdmin,
    PolymorphicMPTTParentModelAdmin,
)

from .models import Route


class BaseRouteChildAdmin(PolymorphicMPTTChildModelAdmin):
    """Common base of all Route subclass admin classes."""
    GENERAL_FIELDSET = (None, {
        'fields': ('slug', 'parent'),
    })

    base_model = Route
    base_fieldsets = (GENERAL_FIELDSET,)


class RouteParentAdmin(PolymorphicMPTTParentModelAdmin):
    """The master admin class for Route."""
    base_model = Route
    list_display = ('__str__', 'actions_column')
    polymorphic_list = True

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',)
        }

    def get_child_models(self):
        """Collect the admin classes of all subclasses of Route."""
        subclasses = self.base_model.__subclasses__()

        child_models = []
        for subclass in subclasses:
            admin_class = subclass.get_admin_class()
            if admin_class is not None:
                child_models.append((subclass, admin_class))
        return child_models

admin.site.register(Route, RouteParentAdmin)
