# django-conman [![Coverage Status](https://img.shields.io/coveralls/meshy/django-conman.svg)](https://coveralls.io/r/meshy/django-conman) [![Build Status](https://travis-ci.org/meshy/django-conman.svg?branch=master)](https://travis-ci.org/meshy/django-conman) [![Wheel Status](https://pypip.in/wheel/django-conman/badge.svg)](https://pypi.python.org/pypi/django-conman/)


A CONtent MANagement system for Django. (Get it?)

Sponsored by [Incuna](http://incuna.com/).

## Requirements

Tested against:
- Python 3.4
- Django 1.7

Requires:
- `django-mptt`

## Install

First install from PyPI:

```
# Doesn't yet work. Not yet on PyPI.
pip install django-conman
```

...or from source:
```
pip install -e git+https://github.com/meshy/django-conman.git#egg=conman
```

## Configure
Add to your `settings.py`:

```
INSTALLED_APPS = [
    ...
    'conman.nav_tree',
]
```

Update your `urls.py` with:

```
urlpatterns = [
    ...  # All other URLS should go above this catch-all.
    url(r'', include('conman.nav_tree.urls')),
]
```

### TODO:
- Add further instructions for installing/using content types
