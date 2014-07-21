from django.core.urlresolvers import resolve


class BaseHandler:
    @classmethod
    def path(cls):
        """Get dotted-path of this class"""
        return '.'.join((cls.__module__, cls.__name__))

    def __init__(self, node):
        self.node = node

    def handle(self, request, path):
        view, args, kwargs = resolve(path, urlconf=self.urlconf)
        return view(request, *args, handler=self, **kwargs)


class SimpleHandler(BaseHandler):
    urlconf = 'nav_tree.handlers.simple.urls'
