# Reference

## `Route`

### `get_absolute_url()`

### `get_ancestors()`

### `get_descendants()`

### `get_handler()`

### `get_subclasses()`

### `handle(...)`

Signature: `handle(self, request, path)`.

### `move_to(...)`

Signature: `move_to(self, new_url, *, move_children)`.

### `swap_with(...)`

Signature: `swap_with(self, other_route, *, move_children)`.

## `Route.objects`

### `best_match_for_path(...)`

Signature: `best_match_for_path(self, path)`.

### `create(...)`

Signature: `create(self, *, url, **kwargs)`.

### `move_branch(...)`

Signature: `move_branch(self, old_url, new_url)`.

## Handlers

### `check(...)`

Classmethod signature: `check(cls, route)`.

### `handle(...)`

Signature: `handle(self, request, path)`.
