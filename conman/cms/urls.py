from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.CMSIndex.as_view(), name='cms-index'),
]
