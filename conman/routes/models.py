from django.core import checks
from django.db import models
from django.db.models.functions import Length
from polymorphic_tree.managers import PolymorphicMPTTModelManager
from polymorphic_tree.models import (
    PolymorphicMPTTModel,
    PolymorphicTreeForeignKey,
)

from .utils import import_from_dotted_path, split_path


class RouteManager(PolymorphicMPTTModelManager):
    """Helpful methods for working with Routes."""
    def best_match_for_path(self, path):
        """
        Return the best match for a path.

        If the path as given is unavailable, continues to search by chopping
        path components off the end.

        Tries hard to avoid unnecessary database lookups by comparing all
        possible matching URL prefixes and choosing the longest match.

        Route.objects.best_match_for_path('/photos/album/2008/09') might return
        the Route with url '/photos/album/'.

        Adapted from feincms/module/page/models.py:71 in FeinCMS v1.9.5.
        """
        paths = split_path(path)

        qs = self.filter(url__in=paths)
        qs = qs.annotate(length=Length('url')).order_by('-length')
        try:
            return qs[0]
        except IndexError:
            msg = 'No matching Route for URL. (Have you made a root Route?)'
            raise self.model.DoesNotExist(msg)


class Route(PolymorphicMPTTModel):
    """
    A Route in a tree of url endpoints.

    A Route can be a Root Route or a Child Route.
    A Root Route has no parent and has an empty slug.
    A Child Route has a parent Route and a slug unique with the parent.
    A Child Route's url is built from its slug and its parent's url.
    """
    parent = PolymorphicTreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
    )
    slug = models.SlugField(max_length=255, default='', help_text='''
        Used to create the location of the Route. The Root Route needs
        "slug" to be blank; all other Routes need a value unique to the parent.
        It can only contain letters, numbers, underscores, or hyphens.
    ''')
    # Cached location in tree. Reflects parent and slug on self and ancestors.
    url = models.TextField(db_index=True, editable=False, unique=True)

    objects = RouteManager()

    class Meta:
        unique_together = ('parent', 'slug')

    def __init__(self, *args, **kwargs):
        """Cache the Route's parent_id and slug."""
        super().__init__(*args, **kwargs)
        self.reset_originals()

    def __str__(self):
        """Display a Route's class and url."""
        return '{} @ {}'.format(self.__class__.__name__, self.url)

    def get_handler_class(self):
        """Import a class from the python path string in `self.handler`."""
        return import_from_dotted_path(self.handler)

    def get_handler(self):
        """
        Get an instance of the handler for this Route instance.

        Multiple calls to this method (on the same instance of Route) will
        return the same instance of handler.
        """
        try:
            return self._handler
        except AttributeError:
            self._handler = self.get_handler_class()(self)
            return self._handler

    def handle(self, request, path):
        """
        Delegate handling the request to the handler.

        The path of this route is chopped off the url to save the handler from
        needing to deal with it. If it really needs it, it will be able to
        derive it from the route (self) that is passed to it on instantiation.
        """
        handler = self.get_handler()
        # Strip the route url from the rest of the path
        path = path[len(self.url) - 1:]
        # Deal with the request
        return handler.handle(request, path)

    def reset_originals(self):
        """
        Cache a copy of the loaded `url` value.

        This is so we can determine if it has been changed on save.
        """
        self._original_parent_id = self.parent_id
        self._original_slug = self.slug

    def save(self, *args, **kwargs):
        """
        Update the `url` attribute of this route and all descendants.

        Quite expensive when called with a route high up in the tree.

        Adapted from feincms/module/page/models.py:248 in FeinCMS v1.9.5.
        """
        is_root = self.parent_id is None
        has_slug = bool(self.slug)

        # Must be one or the other
        if is_root == has_slug:
            raise ValueError('Route can be a root, or have a slug, not both.')

        def make_url(parent_url, slug):
            return '{}{}/'.format(parent_url, slug)

        parent_changed = self._original_parent_id != self.parent_id
        slug_changed = self._original_slug != self.slug
        url_changed = parent_changed or slug_changed or not self.url

        if url_changed:
            self.url = '/' if is_root else make_url(self.parent.url, self.slug)

        super().save(*args, **kwargs)
        self.reset_originals()

        # If the URL changed we need to update all descendants to
        # reflect the changes. Since this is a very expensive operation
        # on large sites we'll check whether our `url` actually changed
        # or if the updates weren't navigation related:
        if not url_changed:
            return

        routes = self.get_descendants().order_by('lft')

        cached_urls = {self.id: self.url}
        for route in routes:
            parent_path = cached_urls[route.parent_id]
            route.url = cached_urls[route.id] = make_url(parent_path, route.slug)

            # Skip this logic on save so we do not recurse.
            super(Route, route).save()
    save.alters_data = True

    @classmethod
    def check(cls, **kwargs):
        """Check that the `handler` attribute exists."""
        errors = super().check(**kwargs)
        if cls != Route and not hasattr(cls, 'handler'):
            errors.append(checks.Error(
                'Route subclasses must have a `handler` attribute',
                hint='`handler` must resolve to a dotted python path',
                obj=cls,
            ))
        return errors
