# Handlers

The base class for handlers is `BaseHandler`. For information on the existing
handlers, see [Handlers (topic guide)](/topics/handlers.md).


## Methods

###  `__init__`

Signature: `__init__(self, route)`

When instantiating a subclass of `BaseHandler`, `route` is a required argument.
This is then saved on the instance as `self.route`, and can be used later from
`handle`.

### `handle`

Signature: `handle(self, request, path)`

Called when someone browses to a `Route`.

Just like a django view, `handle` accepts `request` and is expected to return
an [`HttpResponse`][django-response].

The `path` is relative to the URL of `self.route` (but it will always have a
leading `/`). For example, if the only `Route` in the DB is this one...

```python
route = Route.objects.create(url='/projects/')
```

...then when someone browses to `/projects/conman/`, this method would be
called with `path='/conman/'`.

!!! Note
    The `TemplateHandler` and `ViewHandler` raise a `Resolver404` if the `path`
    is anything other than `/`, but the `URLConfHandler` has the ability to
    deal with other subpaths.

    See [Handlers (topic guide)](/topics/handlers.md).


## Class methods

### `check`

Signature: `check(cls, route)`

Route-subclasses delegate [model-level checks][django-checks] to this method on
their `handler_class`.

This allows handlers to check that their associated `Route` objects are
correctly configured. For example, `TemplateHandler` checks that a
`template_name` attribute exists on associated `Route` subclasses.


[django-checks]: https://docs.djangoproject.com/en/stable/topics/checks/#field-model-manager-and-database-checks
[django-response]: https://docs.djangoproject.com/en/stable/topics/http/views/
