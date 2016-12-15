# django-conman changelog

## Upcoming release

### Backwards incompatible

* Removed `conman.pages` app.
* Removed `slug` and `parent` fields.
* Removed dependency upon `django-polymorphic-tree`.
* Destroyed and recreated migrations.

### Changed

* `url` is now editable, rather than generated in `Route.save()`.
* Moved `RouteManager` into `routes.managers`.

## 0.0.1a1
* Unstable, incomplete API
* Released to claim spot on PyPI
