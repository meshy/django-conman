from django.conf.urls import url


urlpatterns = [
    # Capture urls that are at the root (^$) or end in a slash (^.+/$)
    url(r'^(?P<url>|.+/)$', 'conman.nav_tree.views.node_router'),
]
