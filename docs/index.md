# Django ConMan

Django ConMan is a lightweight content management library for [Django](https://www.djangoproject.com/). It has a very modular structure to allow you to pick-and-choose only the features you need for your site.

## Quick Start

* Install ConMan: `pip install django-conman`
* Add your chosen ConMan modules and [Django Polymorhpic](https://django-polymorphic.readthedocs.org/en/latest/) to `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    'conman.routes',
    'comnan.redirects',

    'polymorphic',

    ...
)
```

* Add ConMan to your base `urls.py` after all other urls:

```python
urlpatterns = [
    ...

    # Must be last to avoid conflicting with other urls.
    url(r'', include('conman.routes.urls')),
]
```
