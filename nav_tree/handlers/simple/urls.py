from django.conf.urls import url

from .views import simple_node_view


urlpatterns = [
    url(r'^$', simple_node_view)
]
