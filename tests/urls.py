from django.conf.urls import include, url


urlpatterns = [
    url(r'', include('conman.routes.urls')),
]
