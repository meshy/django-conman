# Basic HTML Route

In this example, we will create a `Route` subclass with a field containing HTML
content. We're not going to introduce a [rich-text
editor](/tutorials/rich-text.md) yet, but we will show you how to edit the item
in the admin, and render the content when someone browses to the Route's URL.


## Model

In our `models.py` file we'll create a subclass of `Route`, `HTMLRoute`, and
add a `content` field. This is where we will be storing our HTML.

```python
# models.py
from conman.routes.models import Route


class HTMLRoute(Route):
    content = models.TextField()
    template_name = 'html_template.html'
```

We have also included a `template_name` attribute. This is the template that
will be used to render the content.

!!! Note
    As usual, after creating or modifying models, don't forget to [create
    database migrations][django-db-migrations].


## Template

This example is really simple because the template doesn't have to do anything
fancy to render the HTML:

```django
{# html_template.html #}

{{ route.content|safe }}
```

!!! Note
    The [`|safe` filter][django-safe] should be used with extreme caution.
    Marking content from untrusted sources as safe may expose you to [XSS
    attacks][django-xss].


## Admin

To get things working in the admin, we'll register `HTMLRoute` with a subclass
of `RouteChildAdmin`.

```python
# admin.py
from conman.routes.admin import RouteChildAdmin
from django.contrib import admin
from .models import HTMLRoute


@admin.register(HTMLRoute)
class HTMLRouteAdmin(RouteChildAdmin):
    pass
```

!!! Note
    `RouteChildAdmin` is a subclass of django-polymorphic's
    `PolymorphicChildModelAdmin`. For advanced use, please see the
    [django-polymorphic guide to admin integration][django-polymorphic-admin].


[django-db-migrations]: https://docs.djangoproject.com/en/stable/topics/migrations/
[django-polymorphic-admin]: https://django-polymorphic.readthedocs.io/en/stable/admin.html
[django-safe]: https://docs.djangoproject.com/en/stable/ref/templates/builtins/#std:templatefilter-safe
[django-xss]: https://docs.djangoproject.com/en/stable/topics/security/#cross-site-scripting-xss-protection
