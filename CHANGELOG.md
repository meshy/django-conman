# django-conman changelog

## Upcoming release

### Backwards incompatible

* Removed `conman.pages` app.
* Removed `slug` and `parent` fields.
* Removed dependency upon `django-polymorphic-tree`.
* Destroyed and recreated migrations.
* Removed `conman.routes.handlers.SimpleHandler`.
* Removed logic from `conman.routes.handlers.BaseHandler.handle`. Unless
  overridden, this method will now raise a `NotImplementedError`.

### Added

* Added support for django 1.10 (thanks to @Ian-Foote).
* Added `RouteViewHandler`. A handler that delegates request handling to the
  `view` attribute of the `Route`.
* Added `URLConfHandler`. A handler that resolves the provided `path` to a view
  based on the `urlconf` attribute of the `Route`.

### Changed

* `url` is now editable, rather than generated in `Route.save()`.
* Moved `RouteManager` into `routes.managers`.
* `Route` subclasses now have a default `handler`: `RouteViewHandler`.

## 0.0.1a1
* Unstable, incomplete API
* Released to claim spot on PyPI
