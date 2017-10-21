from django.core import checks
from django.shortcuts import render
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
        """Raise an error if a subclass calls handle without defining how."""
        msg = 'Subclasses of `BaseHandler` must implement `handle()`.'
        raise NotImplementedError(msg)


class TemplateHandler(BaseHandler):
    """
    A handler that renders a template.

    Routes using this handler must define `template_name`, which can either
    be a string or list, as accepted by `django.shortcuts.render`.

    Renders the `template_name` of the related Route into an
    `HttpResponse`.
    """
    @classmethod
    def check(cls, route):
        """Ensure route has a template_name attribute."""
        if not hasattr(route, 'template_name'):
            return [checks.Warning(
                '{} must have a `template_name` attribute.'.format(route.__name__),
                hint=('This is a requirement of {}.'.format(cls.__name__)),
                obj=route,
            )]

        return []

    def handle(self, request, path):
        """
        Render a template and return the `HttpResponse` returned.

        Raises `django.core.urlresolvers.Resolver404` if `path` isn't found.
        """
        if path != '/':
            raise Resolver404
        return render(
            request,
            template_name=self.route.template_name,
            context={'route': self.route},
        )


class URLConfHandler(BaseHandler):
    """
    Abstract handler for Routes that resolve views through a urlconf.

    Routes using this handler should define a `urlconf` attribute as a dotted
    path. This will be used to resolve a view when handling requests.

    Views referenced in the `urlconf` will receive `route`, as well as the args
    and kwargs they would expect given their urlpattern.
    """
    @classmethod
    def check(cls, route):
        """Ensure route has a sensible urlconf attribute."""
        if not hasattr(route, 'urlconf'):
            return [checks.Warning(
                '{} must have a `urlconf` attribute.'.format(route.__name__),
                hint=(
                    'The urlconf must be a dotted path. ' +
                    'This is a requirement of {}.'.format(cls.__name__)
                ),
                obj=route,
            )]

        return []

    def handle(self, request, path):
        """
        Resolve `path` to a view, and get it to handle the `request`.

        Returns the `HttpResponse` returned by the view.

        Raises `django.core.urlresolvers.Resolver404` if `path` isn't found.
        """
        view, args, kwargs = resolve(path, urlconf=self.route.urlconf)
        return view(request, *args, route=self.route, **kwargs)


class ViewHandler(BaseHandler):
    """
    Delegates handling to the `view` attribute of the assocated Route.

    Routes using this handler should define a `view` attribute. This will be
    used to handle requests.

    Views will receive `route` as a keyword arg.
    """
    @classmethod
    def check(cls, route):
        """Ensure route has a sensible view attribute."""
        if not hasattr(route, 'view'):
            return [checks.Warning(
                '{} must have a `view` attribute.'.format(route.__name__),
                hint='This is a requirement of {}.'.format(cls.__name__),
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
        # We use `type` here to ensure that we don't access the view as a bound
        # method of the Route, but instead get the view as a function.
        return type(self.route).view(request, route=self.route)
