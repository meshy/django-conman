from django.test import TestCase

from .factories import ChildRouteFactory, RouteFactory
from ..models import Route


class RouteManagerBestMatchForPathTest(TestCase):
    """
    Test Route.objects.best_match_for_path works with perfect url matches.

    All of these tests assert use of only one query:
        * Get the best Route based on url:
            SELECT
                (LENGTH(url)) AS "length",
                <other fields>
            FROM "routes_route"
            WHERE
                "routes_route"."url" IN (
                    '/',
                    '/url/',
                    '/url/split/',
                    '/url/split/into/',
                    '/url/split/into/bits/')
            ORDER BY "length" DESC
            LIMIT 1
    """
    def test_get_root(self):
        """Check a Root Route matches a simple '/' path."""
        root = RouteFactory.create(url='/')
        with self.assertNumQueries(1):
            route = Route.objects.best_match_for_path('/')

        self.assertEqual(route, root)

    def test_get_leaf(self):
        """Check a Route with a slug matches a path of that slug."""
        leaf = ChildRouteFactory.create(slug='leaf')

        with self.assertNumQueries(1):
            route = Route.objects.best_match_for_path('/leaf/')

        self.assertEqual(route, leaf)

    def test_get_leaf_on_branch(self):
        """Check a Route matches a path containing its slug and parent's slug."""
        branch = ChildRouteFactory.create(slug='branch')
        leaf = ChildRouteFactory.create(slug='leaf', parent=branch)

        with self.assertNumQueries(1):
            route = Route.objects.best_match_for_path('/branch/leaf/')

        self.assertEqual(route, leaf)

    def test_get_branch_with_leaf(self):
        """Check a Branch Route matches a path of its slug even if a Leaf exists."""
        branch = ChildRouteFactory.create(slug='branch')
        ChildRouteFactory.create(slug='leaf', parent=branch)

        with self.assertNumQueries(1):
            route = Route.objects.best_match_for_path('/branch/')

        self.assertEqual(route, branch)


class RouteManagerBestMatchForBrokenPathTest(TestCase):
    """
    Test Route.objects.best_match_for_path works without a perfect url match.

    All of these tests assert use of only one query:
        * Get the best Route based on url:
            SELECT
                (LENGTH(url)) AS "length",
                <other fields>
            FROM "routes_route"
            WHERE
                "routes_route"."url" IN (
                    '/',
                    '/url/',
                    '/url/split/',
                    '/url/split/into/',
                    '/url/split/into/bits/')
            ORDER BY "length" DESC
            LIMIT 1
    """
    def test_throw_error_without_match(self):
        """Check Route.DoesNotExist is raised if no Root Route exists."""
        with self.assertNumQueries(1):
            with self.assertRaises(Route.DoesNotExist):
                Route.objects.best_match_for_path('/')

    def test_fall_back_to_root(self):
        """Check the Root Route matches when no better Route is available."""
        root = RouteFactory.create(url='/')

        with self.assertNumQueries(1):
            route = Route.objects.best_match_for_path('/absent-branch/')

        self.assertEqual(route, root)

    def test_fall_back_to_branch(self):
        """Check a Branch Route matches when no Leaf Route matches."""
        branch = ChildRouteFactory.create(slug='branch')

        with self.assertNumQueries(1):
            route = Route.objects.best_match_for_path('/branch/absent-leaf/')

        self.assertEqual(route, branch)
