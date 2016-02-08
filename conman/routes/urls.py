from django.conf.urls import url

from .views import route_router


urlpatterns = [
    # Capture urls that are at the root (^$) or end in a slash (^.+/$)
    url(r'^(?P<url>|.+/)$', route_router),
]
