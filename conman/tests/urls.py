from django.conf.urls import include, url


urlpatterns = [
    url(r'^cms/', include('conman.cms.urls')),
    url(r'', include('conman.routes.urls')),
]
