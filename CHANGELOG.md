# django-conman changelog

## Upcoming release

### Backwards incompatible

* Removed `conman.pages` app.
* Removed `slug` and `parent` fields from Route.
* Removed dependency upon `django-polymorphic-tree`.
* Destroyed and recreated migrations.
* Removed `conman.routes.handlers.SimpleHandler`.
* Removed logic from `conman.routes.handlers.BaseHandler.handle`. Unless
  overridden, this method will now raise a `NotImplementedError`.
* Dropped support for django < 1.10
* Replace `Route.handler` dotted path with `Route.handler_class`.
* Remove `conman.routes.handlers.BaseHandler.path()`.
* Remove `conman.routes.utils.import_from_dotted_path()`.
* Bumped minimum version of `django-polymorphic` to 1.2.
* Change `Route.objects.create` to require and verify a `url` parameter.

### Added

* Added support for django 1.10 (thanks to @Ian-Foote).
* Added support for django 1.11.
* Added `RouteViewHandler`. A handler that delegates request handling to the
  `view` attribute of the `Route`.
* Added `URLConfHandler`. A handler that resolves the provided `path` to a view
  based on the `urlconf` attribute of the `Route`.
* `URLRedirect` has been added to `routes.redirects`. This model can be used to
  represent a URL that redirects to another URL (that is not represented by a
  `Route`). One might expect this to be a URL on an external site.
* Allow `Route` to delegate model checks to the associated handler.
* `Route.objects.move_branch()` can be used to move a `Route` and its
  descendants to another location.
* `Route().move_to(new_url, *, move_children)` can be used to move a `Route`
  and (optionally) it's descendants to another location.
* `Route().swap_with(new_url, *, move_children)` can be used to swap a `Route`
  and (optionally) it's descendants with another `Route`.

### Changed

* `url` is now editable, rather than generated in `Route.save()`.
* Moved `RouteManager` into `routes.managers`.
* `Route` subclasses now have a default `handler`: `RouteViewHandler`.

## 0.0.1a1
* Unstable, incomplete API
* Released to claim spot on PyPI
