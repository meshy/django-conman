from unittest import mock

from django.db import IntegrityError, transaction
from django.test import TestCase
from incuna_test_utils.utils import field_names

from .factories import ChildRouteFactory, RouteFactory
from .. import handlers
from ..models import Route


NODE_BASE_FIELDS = (
    'url',

    # Polymorphic fields
    'polymorphic_ctype',
)


class RouteTest(TestCase):
    """Test Route fields."""
    def test_fields(self):
        """Check the Route model has the expected fields."""
        expected = (
            'id',
            'routeredirect',
            'urlredirect',

            # Incoming foreign keys from subclasses in tests
            'routewithnoview',
            'routewithview',
            'routewithurlconf',
            'routewithnourlconf',
            'urlconfroute',
        ) + NODE_BASE_FIELDS
        fields = field_names(Route)
        self.assertCountEqual(fields, expected)


class RouteUniqueness(TestCase):
    """Check uniqueness conditions on Route are enforced in the DB."""
    def test_unique_url(self):
        """Only one Route can exist with a particular url."""
        Route.objects.create(url='/')

        with self.assertRaises(IntegrityError):
            Route.objects.create(url='/')


class RouteCheckTest(TestCase):
    """Test Route.check()."""
    def test_defer_to_handler(self):
        """Route.check returns the result of Route.handler_class().check()."""
        with mock.patch('conman.routes.models.Route.handler_class') as handler:
            errors = Route.check()

        # Ensure the handler's check method is called...
        handler.check.assert_called_once_with(Route)
        # ... and that the return value is passed back through.
        self.assertEqual(errors, handler.check(Route))


class RouteGetAncestorsTest(TestCase):
    """
    Test Route().get_ancestors().

    All of these tests assert use of only one query:
        * Get the ancestors of a Route:

            SELECT "routes_route"."id",
                   "routes_route"."polymorphic_ctype_id",
                   "routes_route"."url"
              FROM "routes_route"
             WHERE (NOT ("routes_route"."id" = 42)
                    AND "routes_route"."url" IN ('/', '/route43/'))
          ORDER BY "routes_route"."url" ASC
    """
    def test_just_created(self):
        """Until saved, return empty Queryset."""
        route = RouteFactory.build()

        with self.assertNumQueries(0):
            # Presumed nonsense as unsaved, so no query.
            ancestors = list(route.get_ancestors())

        self.assertEqual(ancestors, [])

    def test_no_ancestors(self):
        """Without ancestors, we get an empty result."""
        branch = ChildRouteFactory.create()

        with self.assertNumQueries(1):
            ancestors = list(branch.get_ancestors())

        self.assertEqual(ancestors, [])

    def test_with_ancestors(self):
        """Return ancestors, furthest first."""
        root = RouteFactory.create()
        branch = ChildRouteFactory.create(parent=root)
        leaf = ChildRouteFactory.create(parent=branch)

        with self.assertNumQueries(1):
            ancestors = list(leaf.get_ancestors())

        self.assertEqual(ancestors, [root, branch])

    def test_with_descendants(self):
        """Do not return descendants."""
        branch = ChildRouteFactory.create()
        ChildRouteFactory.create(parent=branch)

        with self.assertNumQueries(1):
            ancestors = list(branch.get_ancestors())

        self.assertEqual(ancestors, [])

    def test_at_root(self):
        """Don't bother looking for ancestors when root Route."""
        root = RouteFactory.create()

        with self.assertNumQueries(0):
            ancestors = list(root.get_ancestors())

        self.assertEqual(ancestors, [])


class RouteGetDescendantsTest(TestCase):
    """
    Test Route().get_descendants().

    All of these tests assert use of only one query:
        * Get the decendants of a Route:

              SELECT "routes_route"."id",
                     "routes_route"."polymorphic_ctype_id",
                     "routes_route"."url"
                FROM "routes_route"
               WHERE (NOT ("routes_route"."id" = 25)
                      AND "routes_route"."url"::text LIKE '/slug25/%')
            ORDER BY "routes_route"."url" ASC
    """
    def test_just_created(self):
        """Until saved, return empty Queryset."""
        branch = RouteFactory.build()

        with self.assertNumQueries(0):
            # Descendants presumed nonsense as unsaved, so no query.
            descendants = list(branch.get_descendants())

        self.assertEqual(descendants, [])

    def test_no_descendants(self):
        """When an Route has no descendants, return no objects."""
        branch = ChildRouteFactory.create()

        with self.assertNumQueries(1):
            descendants = list(branch.get_descendants())

        self.assertEqual(descendants, [])

    def test_descendants(self):
        """When a Route has descendants, return them."""
        root = RouteFactory.create()
        branch = ChildRouteFactory.create(parent=root)

        with self.assertNumQueries(1):
            descendants = list(root.get_descendants())

        self.assertEqual(descendants, [branch])


class RouteGetHandlerTest(TestCase):
    """Make sure that Route.get_handler acts as expected."""
    def test_get_handler(self):
        """We expect an instance of handler instanciated with a Route."""
        class DummyHandler(handlers.BaseHandler):
            pass

        route = RouteFactory.build()
        route.handler_class = DummyHandler

        handler = route.get_handler()
        self.assertIsInstance(handler, DummyHandler)
        self.assertEqual(handler.route, route)

    def test_get_handler_again(self):
        """Make sure we always get the same instance of a handler on a Route."""
        class DummyHandler(handlers.BaseHandler):
            pass

        route = RouteFactory.build()
        route.handler_class = DummyHandler

        first_handler = route.get_handler()
        second_handler = route.get_handler()

        self.assertEqual(first_handler, second_handler)


class RouteHandleTest(TestCase):
    """Check the behaviour of Route.handle()."""
    def test_handle(self):
        """
        Route delegates requests to its handler.

        The Route's url is stripped from the requested url path.
        """
        route = RouteFactory.build(url='/branch/')
        route.handler_class = mock.MagicMock()
        request = mock.Mock()

        result = route.handle(request, '/branch/leaf/')

        expected = route.handler_class(route).handle(request, '/leaf/')
        self.assertEqual(result, expected)


class RouteMoveTo(TestCase):
    """Tests for moving a Route to a new location."""
    def test_without_children(self):
        """When move_children is False, children stay put."""
        branch = RouteFactory.create(url='/old-branch/')
        leaf = ChildRouteFactory.create(slug='leaf', parent=branch)
        new_url = '/new-branch/'

        with self.assertNumQueries(1):
            # UPDATE "routes_route"
            #    SET "polymorphic_ctype_id" = 1,
            #        "url" = '/new-branch/'
            #  WHERE "routes_route"."id" = 42
            branch.move_to(new_url, move_children=False)

        self.assertEqual(branch.url, new_url)
        leaf.refresh_from_db()
        self.assertEqual(leaf.url, '/old-branch/leaf/')

    def test_with_children(self):
        """When move_children is True, children move too."""
        parent = RouteFactory.create(url='/old-branch/')
        child = ChildRouteFactory.create(slug='leaf', parent=parent)
        new_url = '/new-branch/'

        with self.assertNumQueries(1):
            # UPDATE "routes_route"
            #    SET "url" = CONCAT('/new-branch/', SUBSTRING("routes_route"."url", 13))
            #  WHERE "routes_route"."url"::text LIKE '/old-branch/%'
            parent.move_to(new_url, move_children=True)

        # Because the branch object was available, we'd expect it to update.
        self.assertEqual(parent.url, new_url)
        # ...but it's impractical to expect all in-memory objects to update.
        self.assertEqual(child.url, '/old-branch/leaf/')
        # Once refreshed from the db, however, leaf should have updated.
        child.refresh_from_db()
        self.assertEqual(child.url, '/new-branch/leaf/')

    def test_clashing_without_children(self):
        """When clashing without children, don't update to new url."""
        old_url = '/old-url/'
        parent = RouteFactory.create(url=old_url)
        child = ChildRouteFactory.create(slug='leaf', parent=parent)
        occupied_url = '/occupied/'
        RouteFactory.create(url=occupied_url)

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                parent.move_to(occupied_url, move_children=False)

        self.assertEqual(parent.url, old_url)
        child.refresh_from_db()
        self.assertEqual(child.url, '/old-url/leaf/')

    def test_clashing_with_children(self):
        """When clashing with children, don't update urls."""
        old_url = '/old-url/'
        parent = RouteFactory.create(url=old_url)
        child = ChildRouteFactory.create(slug='leaf', parent=parent)
        RouteFactory.create(url='/occupied/leaf/')

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                parent.move_to('/occupied/', move_children=True)

        self.assertEqual(parent.url, old_url)
        child.refresh_from_db()
        self.assertEqual(child.url, '/old-url/leaf/')


class RouteStrTest(TestCase):
    """Make sure that we get something nice when Route is cast to string."""
    def test_root_str(self):
        """A Root Route has a useful string representation."""
        route = RouteFactory.create()

        self.assertEqual(str(route), 'Route @ /')

    def test_child_str(self):
        """A Child Route has a string representation that includes its url."""
        leaf = ChildRouteFactory.create(slug='leaf')

        self.assertEqual(str(leaf), 'Route @ /leaf/')
