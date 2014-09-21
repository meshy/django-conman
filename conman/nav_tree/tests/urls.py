from django.conf.urls import url


def dummy_view():
    """Always gets mocked."""


view_path = 'conman.nav_tree.tests.urls.dummy_view'


urlpatterns = [
    url(r'^$', view_path),
    url(r'^(?P<slug>[a-zA-Z0-9_-]+)/$', view_path),
]
