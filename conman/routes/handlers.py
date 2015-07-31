from django.core.urlresolvers import resolve


class BaseHandler:
    """
    Abstract base class for `Route` handlers.

    Subclasses should define a `urlconf` property as a dotted path. This will
    be used to resolve a view when handling requests.

    Views referenced in the `urlconf` will receive `route` as a kwarg, as
    well as the other args and kwargs they would expect given their urlpattern.
    """
    @classmethod
    def path(cls):
        """Get dotted-path of this class."""
        return '{}.{}'.format(cls.__module__, cls.__name__)

    def __init__(self, route):
        """Store the Route so that we know what we're handling."""
        self.route = route

    def handle(self, request, path):
        """
        Resolve `path` to a view, and get it to handle the `request`.

        Returns the `HttpResponse` returned by the view.

        Raises `django.core.urlresolvers.Resolver404` if `path` isn't found.
        """
        view, args, kwargs = resolve(path, urlconf=self.urlconf)
        return view(request, *args, route=self.route, **kwargs)


class UnboundViewMeta(type):
    """
    Metaclass that wraps the `view` attribute with `staticmethod`.

    This ensures that the method does not bind to the class unintentionally.
    """
    def __new__(cls, name, bases, attrs):
        """Create the new class with a staticmethod view attribute."""
        view = attrs.get('view')
        if view:
            attrs['view'] = staticmethod(view)
        return super().__new__(cls, name, bases, attrs)


class SimpleHandler(BaseHandler, metaclass=UnboundViewMeta):
    """
    Abstract handler for Routes that have one url: `/` relative to the Route.

    Subclasses should define a view on the class as `view`. This will be
    called if the `path` passed to `handle` is `/`.
    """
    urlconf = 'conman.routes.simple.urls'
