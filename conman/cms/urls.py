from django.apps import apps
from django.conf.urls import include, url

from . import views


def app_url(app):
    return url(r'^{}/'.format(app.label), include(app.cms_urls))


def urls():
    app = apps.get_app_config('cms')
    yield url(r'^$', views.CMSIndex.as_view(), name='index')
    yield from map(app_url, app.managed_apps)


urlpatterns = [
    url('', include(list(urls()), namespace='cms')),
]
