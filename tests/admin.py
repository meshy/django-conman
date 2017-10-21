from django.contrib import admin

from conman.routes.admin import RouteChildAdmin

from . import models


route_classes = (
    models.NestedRouteSubclass,
    models.RouteSubclass,
    models.TemplateRoute,
    models.URLConfRoute,
    models.ViewRoute,
)


for route_class in route_classes:
    admin.site.register(route_class, RouteChildAdmin)
