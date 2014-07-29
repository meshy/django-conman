from django.conf.urls import url


def dummy_view(request, node, *args, **kwargs):
    """Always gets mocked."""


urlpatterns = [
    url(r'^$', 'nav_tree.tests.urls.dummy_view'),
    url(r'^(?P<slug>[a-zA-Z0-9_-]+)/$', 'nav_tree.tests.urls.dummy_view'),
]
