# django-conman

[![Coverage Status](https://img.shields.io/coveralls/meshy/django-conman.svg)](https://coveralls.io/r/meshy/django-conman) [![Build Status](https://travis-ci.org/meshy/django-conman.svg?branch=master)](https://travis-ci.org/meshy/django-conman) [![Requirements Status](https://requires.io/github/meshy/django-conman/requirements.svg?branch=master)](https://requires.io/github/meshy/django-conman/requirements/?branch=master)


A CONtent MANagement system for Django. (Get it?)

## Requirements

Tested against:
- Python 3.4, 3.5, 3.6
- Django >=1.10

Requires (should be automatically installed if using `pip`):
- `django-polymorphic`

## Install

```bash
# From PyPI...
pip install django-conman

# ...or from source
pip install -e git+https://github.com/meshy/django-conman.git#egg=conman
```

## Minimal configuration
```python
# settings.py
INSTALLED_APPS += ['conman.routes']
CONMAN_ADMIN_ROUTES = ['myapp.MyRouteSubclass', ...]

# urls.py
urlpatterns = [
    # All other URLS should go above this catch-all.
    url(r'', include('conman.routes.urls')),
]
```

## Basic custom app

In the following example, `MyRoute.trusted_content` contains HTML that is safe
to be rendered directly into a template. Only use [`|safe`][django-safe] with
extreme caution in your own projects.

```python
# my_template.html
{{ route.trusted_content|safe }}


# views.py
from django.shortcuts import render

def my_view(request, route):
    return render(request, 'my_template.html', {'route': route})


# models.py
from conman.routes.models import Route
from . import views

class MyRoute(Route):
    trusted_content = models.TextField()

    view = views.my_view


# admin.py
from conman.routes.admin import RouteChildAdmin
from django.contrib import admin
from .models import MyRoute

@admin.register(MyRoute)
class MyRouteAdmin(RouteChildAdmin):
    pass


# settings.py
CONMAN_ADMIN_ROUTES += ['myapp.MyRoute']
```

A more complex example might use a rich text field such as the `HTMLField` from
[djagno-tinymce][django-tinymce], and be careful to sanitise the HTML with
[bleach][bleach].

[django-safe]: https://docs.djangoproject.com/en/1.8/ref/templates/builtins/#safe
[django-tinymce]: https://github.com/aljosa/django-tinymce
[bleach]: https://github.com/mozilla/bleach
