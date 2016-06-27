# Django Conman

Django Conman is a lightweight content management library for [Django](https://www.djangoproject.com/). It has a very modular structure to allow you to pick-and-choose only the features you need for your site.

## Quick Start

* Install Conman: `pip install django-conman`
* Add your chosen Conman modules and [Django Polymorhpic](https://django-polymorphic.readthedocs.org/en/latest/) to `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    'conman.routes',
    'conman.redirects',

    'polymorphic',

    ...
)
```

* Add Conman to your base `urls.py` after all other urls:

```python
urlpatterns = [
    ...

    # Must be last to avoid conflicting with other urls.
    url(r'', include('conman.routes.urls')),
]
```

* Ensure the Conman database tables exist: `python manage.py migrate`
