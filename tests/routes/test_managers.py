from django.db import IntegrityError, transaction
from django.test import TestCase

from conman.routes.exceptions import InvalidURL
from conman.routes.models import Route

from .factories import ChildRouteFactory, RouteFactory


class RouteManagerBestMatchForPathTest(TestCase):
    """
    Test Route.objects.best_match_for_path works with perfect url matches.

    All of these tests assert use of only one query:
        * Get the best Route based on url:

              SELECT "routes_route"."id",
                     "routes_route"."polymorphic_ctype_id",
                     "routes_route"."url",
                     LENGTH("routes_route"."url") AS "length"
                FROM "routes_route"
               WHERE "routes_route"."url"
                  IN ('/',
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
              SELECT "routes_route"."id",
                     "routes_route"."polymorphic_ctype_id",
                     "routes_route"."url",
                     LENGTH("routes_route"."url") AS "length"
                FROM "routes_route"
               WHERE "routes_route"."url"
                  IN ('/',
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


class RouteManagerCreateTest(TestCase):
    """Route.objects.create() creates Route objects."""
    def test_no_url(self):
        """Without a URL, we see an error."""
        error = "create() missing 1 required keyword-only argument: 'url'"
        with self.assertRaisesMessage(TypeError, error):
            Route.objects.create()

    def test_with_url(self):
        """We can create a Route with a URL."""
        route = Route.objects.create(url='/')  # No exception raised
        self.assertIsInstance(route, Route)

    def test_invalid_url(self):
        """Validation is applied to the URL."""
        with self.assertRaises(InvalidURL):
            Route.objects.create(url='not-a-url')


class RouteManagerMoveBranchTest(TestCase):
    """
    Route.objects.move_branch() moves branches of urls.

    All of these tests assert use of only one query:

        * Replace old url fragment with new one.
            UPDATE "routes_route"
            SET "url" = CONCAT(
                '/destination/',
                SUBSTRING("routes_route"."url", 11))
            WHERE "routes_route"."url"::text LIKE '/original/%'
    """
    def test_destination_vacant(self):
        """A single item can move to an unoccupied URL."""
        route = RouteFactory.create(url='/original/')
        destination = '/target/'

        with self.assertNumQueries(1):
            Route.objects.move_branch(route.url, destination)

        route.refresh_from_db()
        self.assertEqual(route.url, destination)

    def test_destination_occupied(self):
        """A single item cannot move to an occupied URL."""
        original_url = '/original/'
        route = RouteFactory.create(url=original_url)
        occupied = RouteFactory.create(url='/occupied/')

        with transaction.atomic():
            with self.assertNumQueries(1):
                with self.assertRaises(IntegrityError):
                    Route.objects.move_branch(route.url, occupied.url)

        route.refresh_from_db()
        self.assertEqual(route.url, original_url)

    def test_descendant_destination_vacant(self):
        """A branch can move to an unoccupied URL."""
        route = RouteFactory.create(url='/original/')
        child = RouteFactory.create(url='/original/child/')
        destination = '/target/'

        with self.assertNumQueries(1):
            Route.objects.move_branch(route.url, destination)

        route.refresh_from_db()
        self.assertEqual(route.url, destination)
        child.refresh_from_db()
        self.assertEqual(child.url, destination + 'child/')

    def test_descendant_destination_occupied(self):
        """A branch cannot move over an occupied URL."""
        original_url = '/original/'
        route = RouteFactory.create(url=original_url)
        child = RouteFactory.create(url='/original/child/')
        occupied = RouteFactory.create(url='/occupied/child/')

        with transaction.atomic():
            with self.assertNumQueries(1):
                with self.assertRaises(IntegrityError):
                    Route.objects.move_branch(route.url, occupied.url)

        route.refresh_from_db()
        self.assertEqual(route.url, original_url)
        child.refresh_from_db()
        self.assertEqual(child.url, original_url + 'child/')
