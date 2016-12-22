from django.db.models.functions import Length
from polymorphic.managers import PolymorphicManager

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
