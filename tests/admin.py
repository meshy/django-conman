from django.contrib import admin

from conman.routes.admin import RouteChildAdmin

from .models import NestedRouteSubclass, RouteSubclass, URLConfRoute


models = (NestedRouteSubclass, RouteSubclass, URLConfRoute)
for model in models:
    admin.site.register(model, RouteChildAdmin)
