# Admin integration

For this guide, we assume you've already followed the usual [process of
installing Django's admin site][django-admin].

For each subclass of [`Route`](#route) that's going to be editable in the
admin, you'll need to do a little extra configuration.

## An example

Lets assume you have made an app called `my_app` that contains a Route called
`MyRoute`. To allow you to edit this model in the admin, you will need to add a
subclass of `RouteChildAdmin` to `my_app/admin.py`:

```python
from django.contrib import admin
from conman.routes.admin import RouteChildAdmin

@admin.register(MyAdmin)
class MyRouteAdmin(RouteChildAdmin):
    pass
```

## Advanced usage

The admin integration offered by Conman is an extension of that offered by
[django-polymorphic], so for advanced topics, you might want to have a look
there.


[django-admin]: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
[django-get-model]: https://docs.djangoproject.com/en/stable/ref/applications/#django.apps.AppConfig.get_model
[django-polymorphic]: https://django-polymorphic.readthedocs.io/en/stable/admin.html
