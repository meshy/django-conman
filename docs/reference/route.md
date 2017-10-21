# Route

## Fields & attributes

### `url`

The most important part of a `Route` is the `url` field. This reflects the
location where the `Route` can be found.

There are some constraints on the value:

- It must begin and end in forward slash (`/`).
- It cannot contain a question mark (`?`) or hash/pound symbol (`#`).
- It cannot contain consecutive forward slashes (`//`).
- It cannot contain subpaths made exclusively of full-stop/period (eg `/../`).

### `handler_class`

The `handler_class` attribute determines what view is called when someone
browses to a matching URL. See the [handlers topic guide](/topics/handlers.md).


## Methods

### `get_absolute_url()`

Returns the path element of the `Route`'s URL. This is the recommended way to
get the link for a `Route` in templates or similar.

### `get_ancestors()`

Returns a queryset containing the ancestors of the `Route`, sorted
alphabetically.

For example, given these `Route` objects:

```python
r1 = Route.objects.create(url='/')
r2 = Route.objects.create(url='/nested/')
r3 = Route.objects.create(url='/nested/doubly/')
r4 = Route.objects.create(url='/nested/comfortably/')
```

Calling `r4.get_ancestors()` will return the queryset equivalent of `[r1, r2]`.

### `get_descendants()`

Returns a queryset containing the descendants of the `Route`, sorted
alphabetically.

For example, using the `Route` objects above, calling `r2.get_descendants()`
would return the queryset equivalent of `[r3, r4]`

### `get_handler()`

Returns an instance of the [`handler_class`](#handler_class).

If this method is called multiple times on the same `Route` instance, the same
handler will be returned. This call is used by [`handle()`](#handle).

### `handle(...)`

Signature: `handle(self, request, path)`.

Delegates handling of a request to a handler. Returns the HTTP response from
[handler's `handle` method](/reference/handlers.md#handle). Called by the
catch-all view, `route_router`.

### `move_to(...)`

Signature: `move_to(self, new_url, *, move_children)`.

Moves the `Route` to a new URL. If `move_children` is `True`, all child `Route`
objects will be moved too.

If, when moved, there is a clash with an existing `Route`, then an
[`IntegrityError`][django-integrityerror] will be raised.

### `swap_with(...)`

Signature: `swap_with(self, other_route, *, move_children)`.

Swaps one `Route` with another. If `move_children` is `True`, the child `Route`
objects will be moved along with the parents.

When swapping a `Route` with its descendant, `move_children` must be `False`.


## Class methods

### `get_subclasses()`

Returns a generator of all known subclasses. Used to determine which classes
should be configured in the admin.


## `Route.objects`

Because `Route` is a subclass of django-polymorphic's `PolymorphicModel`, the
manager has a more functionality than we've documented here. We've documented
our custom functionality, but for the full picture, please refer to
[django-polymorphic's docs][django-polymorphic-docs].

### `best_match_for_path(...)`

Signature: `best_match_for_path(self, path)`.

Compares to all `Route` urls, and returns the longest matching subpath.

For example, `Route.objects.best_match_for_path('/photos/album/2008/09')` would
return the `Route` with url '/photos/album/' if it was the closest match.

If there is no match, `DoesNotExist` will be raised.

### `create(...)`

Signature: `create(self, *, url, **kwargs)`.

Creates, saves, and returns an instance of `Route` (or, if called on a
subclass, an instance of the subclass).

Differs from [django's `create` manager method][django-manager-create] in that
it requires a `url` keyword argument.

### `move_branch(...)`

Signature: `move_branch(self, old_url, new_url)`.

Moves all `Route` objects starting with `old_url` to `new_url`.

For example, if we have two `Route` objects:

```python
Route(url='/blog/')
Route(url='/blog/conman/')
```

We can move them with `Route.objects.move_branch('/blog/', '/articles/')`, and
will be left with:

```python
Route(url='/articles/')
Route(url='/articles/conman/')
```

They will be moved in one commit. If the move causes a clash with existing
`Route` objects, then an `IntegrityError` will be raised.


[django-integrityerror]: https://docs.djangoproject.com/en/stable/ref/exceptions/#django.db.IntegrityError
[django-manager-create]: https://docs.djangoproject.com/en/stable/ref/models/querysets/#django.db.models.query.QuerySet.create
[django-polymorphic-docs]: https://django-polymorphic.readthedocs.io/en/stable/quickstart.html#using-polymorphic-models
