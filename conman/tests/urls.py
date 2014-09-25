from django.conf.urls import include, url


urlpatterns = [
    url(r'', include('conman.nav_tree.urls')),
]
