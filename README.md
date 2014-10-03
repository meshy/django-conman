# django-conman [![Coverage Status](https://img.shields.io/coveralls/meshy/django-conman.svg)](https://coveralls.io/r/meshy/django-conman) [![Build Status](https://travis-ci.org/meshy/django-conman.svg?branch=master)](https://travis-ci.org/meshy/django-conman) [![Wheel Status](https://pypip.in/wheel/django-conman/badge.svg)](https://pypi.python.org/pypi/django-conman/)


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
INSTALLED_APPS += ['conman.nav_tree']

# urls.py
urlpatterns = [
    # All other URLS should go above this catch-all.
    url(r'', include('conman.nav_tree.urls')),
]
```

## Simple custom app
```python
# models.py
class CustomNode(conman.nav_tree.models.Node):
    """Your data/fields"""

# views.py
class CustomNodeDetail(django.views.generic.DetailView):
    def get_object(self):
        return self.kwargs['node']

# handlers.py
class PageHandler(conman.nav_tree.handlers.SimpleHandler):
    view = CustomNodeDetail.as_view()
```
