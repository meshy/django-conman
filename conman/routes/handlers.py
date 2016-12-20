from django.core import checks
from django.urls import resolve, Resolver404


class BaseHandler:
    """
    Abstract base class for `Route` handlers.

    Subclasses should define `handle`.
    """
    def __init__(self, route):
        """Store the Route so that we know what we're handling."""
        self.route = route

    @classmethod
    def check(cls, route):
        """
        Model-level checks for a Route type delegated to its Handler.

        Custom classes can override this to perform checks on the Routes they
        are attached to.
        """
        return []

    def handle(self, request, path):
        """Raise an error if a subclass calls handle without defining how.."""
        msg = 'Subclasses of `BaseHandler` must implement `handle()`.'
        raise NotImplementedError(msg)


class URLConfHandler(BaseHandler):
    """
    Abstract handler for Routes that resolve views through a urlconf.

    Routes using this handler should define a `urlconf` attribute as a dotted
    path. This will be used to resolve a view when handling requests.

    Views referenced in the `urlconf` will receive `route`, as well as the args
    and kwargs they would expect given their urlpattern.
    """
    def handle(self, request, path):
        """
        Resolve `path` to a view, and get it to handle the `request`.

        Returns the `HttpResponse` returned by the view.

        Raises `django.core.urlresolvers.Resolver404` if `path` isn't found.
        """
        view, args, kwargs = resolve(path, urlconf=self.route.urlconf)
        return view(request, *args, route=self.route, **kwargs)


class RouteViewHandler(BaseHandler):
    """
    Delegates handling to the `view` attribute of the assocated Route.

    Routes using this handler should define a `view` attribute. This will be
    used to handle requests.

    Views will receive `route` as a keyword arg.
    """
    @classmethod
    def check(cls, route):
        """Ensure route has a sensible view attribute."""
        route_name = route.__name__
        if not hasattr(route, 'view'):
            return [checks.Error(
                '{} must have a `view` attribute.'.format(route_name),
                hint='This is a requirement of {}.'.format(cls.__name__),
                obj=route,
            )]

        if not isinstance(vars(route)['view'], staticmethod):
            return [checks.Error(
                '{}.view must be a staticmethod.'.format(route_name),
                hint='Try `view = staticmethod(myview)`.'.format(cls),
                obj=route,
            )]

        return []

    def handle(self, request, path):
        """
        Handle the request using the `view` attribute of the associated route.

        Returns the `HttpResponse` returned by the view.

        `path` is trimmed by `Route.handle()` before it is passed in.
        This means that when `path != '/'`, the url of the request does not
        correctly match that of the `Route`. In this case, we will raise
        `django.core.urlresolvers.Resolver404`.
        """
        if path != '/':
            raise Resolver404
        view = self.route.view
        return view(request, route=self.route)
