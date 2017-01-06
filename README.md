# django-conman

[![Coverage Status](https://img.shields.io/coveralls/meshy/django-conman.svg)](https://coveralls.io/r/meshy/django-conman) [![Build Status](https://travis-ci.org/meshy/django-conman.svg?branch=master)](https://travis-ci.org/meshy/django-conman) [![Requirements Status](https://requires.io/github/meshy/django-conman/requirements.svg?branch=master)](https://requires.io/github/meshy/django-conman/requirements/?branch=master)


A CONtent MANagement system for Django. (Get it?)

Sponsored by [Incuna](http://incuna.com/).

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

## Configure
```python
# settings.py
INSTALLED_APPS += ['conman.routes']

# urls.py
urlpatterns = [
    # All other URLS should go above this catch-all.
    url(r'', include('conman.routes.urls')),
]
```

## Basic custom app
```python
# models.py
class ExampleRoute(conman.routes.models.Route):
    # Your data/fields here
    ...
    view = ExampleRouteDetail.as_view()

# views.py
class ExampleRouteDetail(django.views.generic.DetailView):
    def get_object(self):
        return self.kwargs['route']
```
