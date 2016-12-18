from unittest import mock

from django.conf.urls import url


dummy_view = mock.MagicMock()


urlpatterns = [
    url(r'^$', dummy_view),
    url(r'^(?P<slug>[a-zA-Z0-9_-]+)/$', dummy_view),
]
