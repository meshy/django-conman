from django.contrib import admin

from conman.routes.admin import RouteChildAdmin

from .models import (
    NestedRouteSubclass,
    RouteSubclass,
    TemplateRoute,
    URLConfRoute,
)


models = (NestedRouteSubclass, RouteSubclass, TemplateRoute, URLConfRoute)
for model in models:
    admin.site.register(model, RouteChildAdmin)
