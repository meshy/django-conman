# Handlers

In Conman, each `Route` must have a `handler_class` attribute. It is used to
handle those requests that best match the `Route.url`. Each handler delegates
request handling differently. There are three handler classes:

## `TemplateHandler`

`TemplateHandler` is the simplest handler, and is the default for all `Route`
classes.

It renders a template, and the resulting response is returned to the browser.
The related `Route` is added to the template context as `route`.

To let the hander know which template to render, set `template_name` on the
`Route`. eg:

```python
from conman.routes.handlers import TemplateHandler
from conman.routes.models import Route

class ExampleRoute(Route):
    handler_class = TemplateHandler  # Not required, already default.
    template_name = 'my_app/my_template.html'
```

If the browsed URL does not exacly match the `url` attribute of the `Route`,
then `TemplateHandler` will raise a [`Resolver404`.][django-resolver404].

## `ViewHandler`

`ViewHandler` delegates handling of the request to a django view (so it can
respond to POST requests, do extra queries, add more to the context, etc).

Define the delegated view as an attribute on the `Route`. eg:

```python
from conman.routes.handlers import ViewHandler
from conman.routes.models import Route
from .views import my_view

class ExampleRoute(Route):
    handler_class = ViewHandler
    view = my_view
```

If the browsed URL does not exacly match the `url` attribute of the `Route`,
then `ViewHandler` will raise a [`Resolver404`.][django-resolver404].

## `URLConfHandler`

`URLConfHandler` offers the most flexibility, as it can delegate to one of a
number of views depending on how the browsed URL matches the `url` attribute of
the `Route`.

The flexibility comes with a little more setup, as you need to define a URL
config to associate with your `Route`.

```python
# path/to/urls.py
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.list_view),
    url(r'^add/$', views.add_view),
    url(r'^(?P<pk>\d+)/', include([
        url(r'^$', views.detail_view),
        url(r'^delete', views.delete_view),
        url(r'^update', views.update_view),
    ])),
]


# models.py
from conman.routes.handlers import URLConfHandler
from conman.routes.models import Route

class ExampleRoute(Route):
    handler_class = URLConfHandler
    urlconf = 'path.to.urls'
```

So now if you created a route:

```python
my_route = ExampleRoute.objects.create(url='/stuff/')
```

And you browsed to `/stuff/add/`, `views.add_view` would be called with
`request, route` as keyword arguments.


[django-resolver404]: https://docs.djangoproject.com/en/stable/ref/exceptions/#resolver404
