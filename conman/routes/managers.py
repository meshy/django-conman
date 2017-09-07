from django.core.exceptions import ValidationError
from django.db.models import Value
from django.db.models.functions import Concat, Length, Substr
from polymorphic.managers import PolymorphicManager

from .exceptions import InvalidURL
from .utils import split_path


class RouteManager(PolymorphicManager):
    """Helpful methods for working with Routes."""
    silence_use_for_related_fields_deprecation = True

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

    def create(self, *, url, **kwargs):
        """Require (and validate) 'url' when creating Routes."""
        validators = self.model._meta.get_field('url').validators
        try:
            for validator in validators:
                validator(url)
        except ValidationError as e:
            raise InvalidURL(e.message)
        return super().create(url=url, **kwargs)

    def move_branch(self, old_url, new_url):
        """
        Move a Route and all descendants to a new URL.

        eg: Given:

            Route(url='/blog/')
            Route(url='/blog/conman/')

        We can do:

            >>> Route.objects.move_branch('/blog/', '/articles/')

        Now we have:

            Route(url='/articles/')
            Route(url='/articles/conman/')

        Movement will be atomic. This means that failure to move any one Route
        will cause all movement to fail. A conflicting URL will cause an
        IntegrityError.
        """
        self.filter(url__startswith=old_url).update(url=Concat(
            Value(new_url),
            Substr('url', len(old_url) + 1),  # 1 indexed
        ))
