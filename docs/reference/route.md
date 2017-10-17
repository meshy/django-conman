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

Returns an instance of the `handler_class`.

### `handle(...)`

Signature: `handle(self, request, path)`.

### `move_to(...)`

Signature: `move_to(self, new_url, *, move_children)`.

### `swap_with(...)`

Signature: `swap_with(self, other_route, *, move_children)`.

## Class methods

### `get_subclasses()`

Returns a generator of all known subclasses. Used to determine which classes
should be configured in the admin.

## `Route.objects`


### `best_match_for_path(...)`

Signature: `best_match_for_path(self, path)`.

### `create(...)`

Signature: `create(self, *, url, **kwargs)`.

### `move_branch(...)`

Signature: `move_branch(self, old_url, new_url)`.
