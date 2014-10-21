# django-conman

[![Coverage Status](https://img.shields.io/coveralls/meshy/django-conman.svg)](https://coveralls.io/r/meshy/django-conman) [![Build Status](https://travis-ci.org/meshy/django-conman.svg?branch=master)](https://travis-ci.org/meshy/django-conman) [![Wheel Status](https://pypip.in/wheel/django-conman/badge.svg)](https://pypi.python.org/pypi/django-conman/) [![Requirements Status](https://requires.io/github/meshy/django-conman/requirements.svg?branch=master)](https://requires.io/github/meshy/django-conman/requirements/?branch=master)


A CONtent MANagement system for Django. (Get it?)

Sponsored by [Incuna](http://incuna.com/).

## Requirements

Tested against:
- Python 3.4
- Django 1.7

Requires:
- `django-mptt`
- `django-polymorphic-tree`
- `django-sirtrevor`

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
class ExampleNode(conman.routes.models.Node):
    handler = ExampleHandler.path()
    # Your data/fields here

# handlers.py
class ExampleHandler(conman.routes.handlers.SimpleHandler):
    view = ExampleNodeDetail.as_view()

# views.py
class ExampleNodeDetail(django.views.generic.DetailView):
    def get_object(self):
        return self.kwargs['node']
```
