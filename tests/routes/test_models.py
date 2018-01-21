from unittest import mock

from django import forms
from django.db import IntegrityError, transaction
from django.test import TestCase
from incuna_test_utils.utils import field_names

from conman.routes import handlers
from conman.routes.models import Route
from tests.models import NestedRouteSubclass, RouteSubclass

from .factories import ChildRouteFactory, RouteFactory


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
            # Incoming foreign keys from subclasses
            'routeredirect',  # conman.redirects.models.RouteRedirect
            'routesubclass',  # tests.models.RouteSubclass
            'templateroute',  # tests.models.TemplateRoute
            'urlconfroute',  # tests.models.URLConfRoute
            'urlredirect',  # conman.redirects.models.URLRedirect
            'viewroute',  # tests.models.ViewRoute
        ) + NODE_BASE_FIELDS
        fields = field_names(Route)
        self.assertCountEqual(fields, expected)

    def test_get_absolute_url(self):
        """Route.get_absolute_url returns the url of the Route."""
        route = RouteFactory.build(url='/testing/')
        self.assertEqual(route.get_absolute_url(), route.url)

    def test_url_form_widget(self):
        """Route.url uses the single-line TextInput widget."""
        widget = Route._meta.get_field('url').formfield().widget
        self.assertIsInstance(widget, forms.TextInput)

    def test_level(self):
        """Route.level is based on the url field, and is zero-indexed."""
        urls = (
            (0, '/'),
            (1, '/branch/'),
            (2, '/branch/leaf/'),
        )
        for level, url in urls:
            with self.subTest(url=url):
                route = RouteFactory.build(url=url)
                self.assertEqual(route.level, level)


class RouteUniquenessTest(TestCase):
    """Check uniqueness conditions on Route are enforced in the DB."""
    def test_unique_url(self):
        """Only one Route can exist with a particular url."""
        Route.objects.create(url='/')

        with self.assertRaises(IntegrityError):
            Route.objects.create(url='/')


class RouteCheckTest(TestCase):
    """Test Route.check()."""
    def test_route_subclass(self):
        """Route.check returns handler_class().check() on subclasses."""
        with mock.patch.object(RouteSubclass, 'handler_class') as handler:
            errors = RouteSubclass.check()

        # Ensure the handler's check method is called...
        handler.check.assert_called_once_with(RouteSubclass)
        # ... and that the return value is passed back through.
        self.assertEqual(errors, handler.check(RouteSubclass))

    def test_base_route_class(self):
        """Route.check doesn't call handler_class().check on Route."""
        with mock.patch.object(Route, 'handler_class') as handler:
            errors = Route.check()

        self.assertFalse(handler.check.called)
        self.assertEqual(errors, [])


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
        """Until saved, raise an error."""
        route = RouteFactory.build()

        # Presumed nonsense as unsaved, so no query.
        with self.assertNumQueries(0):
            with self.assertRaises(AssertionError):
                route.get_ancestors()

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

        # Descendants presumed nonsense as unsaved, so no query.
        with self.assertNumQueries(0):
            with self.assertRaises(AssertionError):
                branch.get_descendants()

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

    def test_default_handler(self):
        """Ensure the default handler is TemplateHandler."""
        route = RouteFactory.build()
        handler = route.get_handler()
        self.assertIsInstance(handler, handlers.TemplateHandler)


class RouteGetSubclassesTest(TestCase):
    """Check behaviour of Route.get_subclasses()."""
    def test_subclasses(self):
        """Direct subclasses of Route are caught."""
        subclasses = Route.get_subclasses()
        self.assertIn(RouteSubclass, subclasses)

    def test_nested_subclasses(self):
        """Nested subclasses of Route are caught."""
        subclasses = Route.get_subclasses()
        self.assertIn(NestedRouteSubclass, subclasses)


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


class RouteMoveToTest(TestCase):
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


class RouteSwapWithTest(TestCase):
    """Tests for Route.swap_with()."""
    def test_peer_with_different_children(self):
        """Test swapping route branches with children."""
        parent_1 = RouteFactory.create(url='/a/')
        child_1 = ChildRouteFactory(parent=parent_1, slug='1')
        parent_2 = RouteFactory.create(url='/b/')
        child_2 = ChildRouteFactory(parent=parent_2, slug='2')

        with self.assertNumQueries(3):
            # # Move /a/ aside to a UUID
            # UPDATE "routes_route"
            #    SET "url" = CONCAT(
            #                'a-uuid',
            #                SUBSTRING("routes_route"."url", 4))
            #  WHERE "routes_route"."url"::text LIKE '/a/%'
            #
            # # Move /b/ to /a/
            # UPDATE "routes_route"
            #    SET "url" = CONCAT(
            #                '/a/',
            #                SUBSTRING("routes_route"."url", 4))
            #  WHERE "routes_route"."url"::text LIKE '/b/%'
            #
            # # Move original /a/ (now at UUID) to /b/
            # UPDATE "routes_route"
            #    SET "url" = CONCAT(
            #                '/b/',
            #                SUBSTRING("routes_route"."url", 37))
            #  WHERE "routes_route"."url"::text LIKE 'a-uuid%'
            parent_1.swap_with(parent_2, move_children=True)

        # It's unreasonable to expect the children in memory to update.
        self.assertEqual(child_1.url, '/a/1/')
        self.assertEqual(child_2.url, '/b/2/')

        # ...but once fetched from the DB, we should see the new URLs.
        child_1.refresh_from_db()
        child_2.refresh_from_db()
        self.assertEqual(child_1.url, '/b/1/')
        self.assertEqual(child_2.url, '/a/2/')

    def test_peer_with_similar_children(self):
        """Test swapping route branches where children may clash."""
        parent_1 = RouteFactory.create(url='/a/')
        child_1 = ChildRouteFactory(parent=parent_1, slug='child')
        parent_2 = RouteFactory.create(url='/b/')
        child_2 = ChildRouteFactory(parent=parent_2, slug='child')

        with self.assertNumQueries(3):
            # # Move /a/ aside to a UUID
            # UPDATE "routes_route"
            #    SET "url" = CONCAT(
            #                'a-uuid',
            #                SUBSTRING("routes_route"."url", 4))
            #  WHERE "routes_route"."url"::text LIKE '/a/%'
            #
            # # Move /b/ to /a/
            # UPDATE "routes_route"
            #    SET "url" = CONCAT(
            #                '/a/',
            #                SUBSTRING("routes_route"."url", 4))
            #  WHERE "routes_route"."url"::text LIKE '/b/%'
            #
            # # Move original /a/ (now at UUID) to /b/
            # UPDATE "routes_route"
            #    SET "url" = CONCAT(
            #                '/b/',
            #                SUBSTRING("routes_route"."url", 37))
            #  WHERE "routes_route"."url"::text LIKE 'a-uuid%'
            parent_1.swap_with(parent_2, move_children=True)

        # Once fetched from the DB, the new URLs should have been applied.
        child_1.refresh_from_db()
        child_2.refresh_from_db()
        self.assertEqual(child_1.url, '/b/child/')
        self.assertEqual(child_2.url, '/a/child/')

    def test_peer_without_children(self):
        """Test swapping route branches without children."""
        route_1 = RouteFactory.create(url='/a/')
        route_2 = RouteFactory.create(url='/b/')

        with self.assertNumQueries(3):
            # UPDATE "routes_route"
            #    SET "polymorphic_ctype_id" = 1,
            #        "url" = 'a-uuid'
            #  WHERE "routes_route"."id" = 1
            #
            # UPDATE "routes_route"
            #    SET "polymorphic_ctype_id" = 1,
            #        "url" = '/a/'
            #  WHERE "routes_route"."id" = 2
            #
            # UPDATE "routes_route"
            #    SET "polymorphic_ctype_id" = 1,
            #        "url" = '/b/'
            #  WHERE "routes_route"."id" = 1
            route_1.swap_with(route_2, move_children=False)

        # The URLs of the objects in memory have changed.
        self.assertEqual(route_1.url, '/b/')
        self.assertEqual(route_2.url, '/a/')

        # The URLs of the objects in the DB have changed.
        route_1.refresh_from_db()
        route_2.refresh_from_db()
        self.assertEqual(route_1.url, '/b/')
        self.assertEqual(route_2.url, '/a/')

    def test_descendant_with_children(self):
        """An ancestor cannot swap with a descendant if children are included."""
        branch = RouteFactory.create(url='/branch/')
        leaf = ChildRouteFactory.create(parent=branch, slug='leaf')

        msg = 'Cannot move children when swapping ancestors with descendants.'
        with self.assertNumQueries(0):
            with self.assertRaisesMessage(ValueError, msg):
                branch.swap_with(leaf, move_children=True)

        # The URLs of the objects in memory remain unchanged.
        self.assertEqual(branch.url, '/branch/')
        self.assertEqual(leaf.url, '/branch/leaf/')

    def test_descendant_without_children(self):
        """An ancestor can swap with a descendant if children are excluded."""
        branch = RouteFactory.create(url='/branch/')
        leaf = ChildRouteFactory.create(parent=branch, slug='leaf')

        with self.assertNumQueries(3):
            # UPDATE "routes_route"
            #    SET "polymorphic_ctype_id" = 1,
            #        "url" = 'a-uuid'
            #  WHERE "routes_route"."id" = 1
            #
            # UPDATE "routes_route"
            #    SET "polymorphic_ctype_id" = 1,
            #        "url" = '/branch/'
            #  WHERE "routes_route"."id" = 2
            #
            # UPDATE "routes_route"
            #    SET "polymorphic_ctype_id" = 1,
            #        "url" = '/branch/leaf/'
            #  WHERE "routes_route"."id" = 1
            branch.swap_with(leaf, move_children=False)

        # The URLs of the objects in memory have changed.
        self.assertEqual(branch.url, '/branch/leaf/')
        self.assertEqual(leaf.url, '/branch/')

        # The URLs of the objects in the DB have changed.
        branch.refresh_from_db()
        leaf.refresh_from_db()
        self.assertEqual(branch.url, '/branch/leaf/')
        self.assertEqual(leaf.url, '/branch/')

    def test_unsaved_routes(self):
        """If either route is unsaved, raise an exception."""
        route_1 = RouteFactory.create(url='/a/')
        route_2 = RouteFactory.build(url='/b/')

        with self.assertNumQueries(0):
            with self.assertRaises(AssertionError):
                route_1.swap_with(route_2, move_children=True)
            with self.assertRaises(AssertionError):
                route_2.swap_with(route_1, move_children=True)


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
