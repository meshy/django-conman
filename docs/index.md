# Django Conman

Conman is a lightweight content management library for [Django][django].

It allows you to manage your site's URLs in the database, but doesn't dictate
the shape of your data. Instead, you create types of content that can be
associated with the URLs, and views to display them. This leads to a little
extra setup, but is very flexible.

## Requirements

- **Python 3.4+**. Python 2 is **not** supported.
- **Django 1.10+**. Support will only continue for [versions that are supported
  upstream][django-supported-versions].

## Installation & configuration

### Installation

The most reliable way to install the latest version of django-conman is to use
[pip][pip] to install from [PyPI][pypi]:

```bash
pip install django-conman
```

If you wish to test out the latest development version instead, you can
install directly from [the github repo][github-repo]:

```bash
pip install -e git+https://github.com/meshy/django-conman.git#egg=django-conman
```

### URL configuration

Add to your root `urls.py` after all other urls:

```python
urlpatterns = [
    # Must be last to avoid conflicting with other urls.
    url(r'', include('conman.routes.urls')),
]
```

### Settings


Add Conman and [Django Polymorhpic][django-polymorphic] to `INSTALLED_APPS`.

```python
INSTALLED_APPS += (
    'conman.routes',
    'conman.redirects',  # Optional, see below.
    'polymorphic',
)
```
!!! Note
    For more information about `'conman.redirects'`, see the [Redirects topic
    guide](/topics/redirects.md).

    You are likely to be adding more apps here, as few `Route` subclasses are
    provided out of the box. See the [Routes topic guide](/topics/routes.md).

    To create your own, see the [Creating custom
    routes](/tutorials/custom_routes.md) tutorial.


### Migrations

Create the database tables:

```bash
python manage.py migrate
```

### Admin integration

If you're using django's admin, see the [Admin integration topic
guide](/topics/admin.md).


[content-types]: https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/
[django]: https://www.djangoproject.com/
[django-polymorphic]: https://django-polymorphic.readthedocs.org/en/latest/
[django-supported-versions]: https://www.djangoproject.com/download/#supported-versions
[github-repo]: https://github.com/meshy/django-conman
[pip]: https://pip.pypa.io/en/latest/
[pypi]: https://pypi.python.org/
