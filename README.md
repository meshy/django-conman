# django-conman <br><small>A CONtent MANagement system for django (get it?).</small>

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
pip install -e git+https://github.com/incuna/django-conman.git#egg=conman
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
