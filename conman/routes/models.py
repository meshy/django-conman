import uuid

from django.db import IntegrityError, models
from django.utils.translation import ugettext_lazy as _
from polymorphic.models import PolymorphicModel

from .handlers import RouteViewHandler
from .managers import RouteManager
from .utils import split_path
from .validators import (
    validate_end_in_slash,
    validate_no_dotty_subpaths,
    validate_no_double_slashes,
    validate_no_hash_symbol,
    validate_no_questionmark,
    validate_start_in_slash,
)


class Route(PolymorphicModel):
    """A Route in a tree of url endpoints."""
    url = models.TextField(
        db_index=True,
        validators=[
            validate_end_in_slash,
            validate_start_in_slash,
            validate_no_dotty_subpaths,
            validate_no_double_slashes,
            validate_no_hash_symbol,
            validate_no_questionmark,
        ],
        unique=True,
    )

    objects = RouteManager()
    handler_class = RouteViewHandler

    def __str__(self):
        """Display a Route's class and url."""
        return '{} @ {}'.format(self.__class__.__name__, self.url)

    @classmethod
    def check(cls):
        """Delegate model checks to the handler."""
        # Skip checks on the base class. They're intended for subclasses.
        if cls == Route:
            return []
        return cls.handler_class.check(cls)

    def get_absolute_url(self):
        """Return the path element of the URL for this Route."""
        return self.url

    def get_ancestors(self):
        """Get all the ancestors of this Route."""
        assert self.pk is not None  # Ensure object has been saved.

        paths = split_path(self.url)[:-1]
        return (
            Route.objects
            .exclude(pk=self.pk)
            .filter(url__in=paths)
            .order_by('url')
        )

    def get_descendants(self):
        """Get all the descendants of this Route."""
        assert self.pk is not None  # Ensure object has been saved.

        return (
            Route.objects
            .exclude(pk=self.pk)
            .filter(url__startswith=self.url)
            .order_by('url')
        )

    def get_handler(self):
        """
        Get an instance of the handler for this Route instance.

        Multiple calls to this method (on the same instance of Route) will
        return the same instance of handler.
        """
        try:
            return self._handler
        except AttributeError:
            self._handler = self.handler_class(self)
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

    def move_to(self, new_url, *, move_children):
        """
        Move this Route to a new url.

        Requires `move_children` as a keyword argument. If True, all child
        Routes will be moved along with this parent. Otherwise, when False, any
        and all children will remain where they are.

        In the event of a clash, an IntegrityError will be raised.
        """
        if move_children:
            # Delegate movement to manager method.
            Route.objects.move_branch(self.url, new_url)
            # Update URL of this object before returning.
            # (No need to save, the DB value has already changed.)
            self.url = new_url
        else:
            old_url, self.url = self.url, new_url
            try:
                self.save()
            except IntegrityError:
                self.url = old_url
                raise

    def swap_with(self, other_route, *, move_children):
        """
        Swap this Route's URL with that of another Route.

        Requires `move_children` as a keyword argument. When `True`, all
        descendant routes will be moved along with the parents. When `False`,
        they will remain where they are, and only the parents will be swapped.

        When one of the `Routes` is a descendant of the other, `move_children`
        must be `False`.

        If DEFERRED unique contrstraints get supported in django, we might
        benefit from revisiting how this works (ie: dropping the UUID).

        See https://code.djangoproject.com/ticket/20581.
        """
        # Ensure saved to DB.
        assert self.pk is not None and other_route.pk is not None

        urls = sorted((self.url, other_route.url))
        if move_children and urls[1].startswith(urls[0]):
            msg = _('Cannot move children when swapping ancestors with descendants.')
            raise ValueError(msg)

        tmp_path = str(uuid.uuid4())
        if move_children:
            # Delegate movement to manager method. A UUID is used as an
            # intermediary URL to avoid unique constraints.
            Route.objects.move_branch(self.url, tmp_path)
            Route.objects.move_branch(other_route.url, self.url)
            Route.objects.move_branch(tmp_path, other_route.url)
            # Update URL of these objects before returning.
            # (No need to save, the DB value has already changed.)
            other_route.url, self.url = self.url, other_route.url
        else:
            original_url, self.url = self.url, tmp_path
            self.save()
            self.url, other_route.url = other_route.url, original_url
            other_route.save()
            self.save()
