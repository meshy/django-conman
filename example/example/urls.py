from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url('^admin/', include(admin.site.urls)),
    url(r'', include('conman.routes.urls')),
]
