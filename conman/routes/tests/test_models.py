from unittest import mock

from django.db.utils import IntegrityError
from django.test import TestCase
from incuna_test_utils.utils import field_names

from .factories import (
    ChildRouteFactory,
    RootRouteFactory,
    RouteFactory,
    SiteFactory,
)
from .. import handlers
from ..models import Route


NODE_BASE_FIELDS = (
    'parent',
    'slug',
    'site',
    'url',

    # Polymorphic fields
    'polymorphic_ctype',

    # Incoming foreign keys
    'children',  # FK from self. The other end of "parent".
)


class RouteTest(TestCase):
    """Test Route fields."""
    def test_fields(self):
        """Check the Route model has the expected fields."""
        expected = (
            'id',
            'routeredirect',
            'page',

            # Incoming foreign keys from subclasses in tests
            'routewithhandler',
            'routewithouthandler',
        ) + NODE_BASE_FIELDS
        fields = field_names(Route)
        self.assertCountEqual(fields, expected)


class RouteValidateOnSave(TestCase):
    """Check validation of Route slugs and ancestry on save."""
    def test_create_root_with_slug(self):
        """Root must not have a slug."""
        root_route = RouteFactory.build(slug='slug', parent=None)

        with self.assertRaises(ValueError):
            root_route.save()

    def test_create_leaf_without_slug(self):
        """Leaf Routes must have a slug."""
        root_route = RootRouteFactory.create()
        leaf = RouteFactory.build(slug='', parent=root_route)

        with self.assertRaises(ValueError):
            leaf.save()


class RouteUniqueness(TestCase):
    """Check uniqueness conditions on Route are enforced in the DB."""
    def test_unique_slug_per_parent(self):
        """Two Routes cannot share the same slug and parent Route."""
        slug = 'slug'
        root_route = RootRouteFactory.create()
        RouteFactory.create(slug=slug, parent=root_route)

        with self.assertRaises(IntegrityError):
            RouteFactory.create(slug=slug, parent=root_route)

    def test_unique_root_url(self):
        """Only one Route can exist with an empty slug."""
        site = SiteFactory.create()
        Route.objects.create(slug='', site=site)

        with self.assertRaises(IntegrityError):
            Route.objects.create(slug='', site=site)


class RouteSkipUpdateWithoutChange(TestCase):
    """Be frugal with DB hits when saving unmodified Routes."""
    def test_no_update_without_changes(self):
        """Saving unchanged Route shouldn't query parent to rebuild the url."""
        branch = ChildRouteFactory.create(slug='branch')
        branch = Route.objects.get(pk=branch.pk)
        # Prove that no attempt is made to update descendants.
        with self.assertNumQueries(1):
            # One query:
            # * Update the root.
            branch.save()

    def test_no_update_on_resave(self):
        """Resaving changed Route should only update descendants once."""
        branch = ChildRouteFactory.create(slug='branch')
        RouteFactory.create(slug='leaf', parent=branch)
        branch.slug = 'new_slug'
        branch.save()

        # Prove that no attempt is made to update descendants.
        with self.assertNumQueries(1):
            # One query:
            # * Update the root.
            branch.save()


class RouteCachesURLOnCreateTest(TestCase):
    """Make sure Route urls are built correctly on create."""
    def test_create_root(self):
        """Root Route should be at the root url."""
        root = RootRouteFactory.create()
        self.assertEqual(root.url, '/')

    def test_create_leaf_on_root(self):
        """Children of the root should be at /<slug>/."""
        leaf = ChildRouteFactory.create(slug='leaf')

        self.assertEqual(leaf.url, '/leaf/')

    def test_create_child_of_child(self):
        """Children of children should be at /<parent-slug>/<slug>/."""
        branch = ChildRouteFactory.create(slug='branch')
        leaf = RouteFactory.create(slug='leaf', parent=branch)

        self.assertEqual(leaf.url, '/branch/leaf/')


class RouteCachesURLOnRenameTest(TestCase):
    """Make sure Route urls are updated correctly when a slug changes."""
    def test_rename_leaf(self):
        """Changing slug on a leaf should update the cached url."""
        leaf = ChildRouteFactory.create(slug='foo')

        leaf.slug = 'bar'
        leaf.save()

        self.assertEqual(leaf.url, '/bar/')

    def test_rename_branch(self):
        """Changing a branch slug should update the child url."""
        branch = ChildRouteFactory.create(slug='foo')
        leaf = RouteFactory.create(slug='leaf', parent=branch)

        branch.slug = 'bar'
        branch.save()

        leaf = Route.objects.get(pk=leaf.pk)
        self.assertEqual(leaf.url, '/bar/leaf/')

    def test_rename_trunk(self):
        """Changing a trunk slug should update the grandchild url."""
        trunk = ChildRouteFactory.create(slug='foo')
        branch = RouteFactory.create(slug='branch', parent=trunk)
        leaf = RouteFactory.create(slug='leaf', parent=branch)

        trunk.slug = 'bar'
        trunk.save()

        leaf = Route.objects.get(pk=leaf.pk)
        self.assertEqual(leaf.url, '/bar/branch/leaf/')


class RouteCachesURLOnMoveTest(TestCase):
    """Make sure Route urls are updated correctly when moved in the tree."""
    def test_move_leaf(self):
        """Moving a leaf onto a new branch should update the cached url."""
        branch = ChildRouteFactory.create(slug='foo')
        leaf = RouteFactory.create(slug='leaf', parent=branch)

        new_branch = ChildRouteFactory.create(slug='bar')
        leaf.parent = new_branch
        leaf.save()

        self.assertEqual(leaf.url, '/bar/leaf/')

    def test_move_branch(self):
        """Moving a branch onto a new trunk should update the leaf urls."""
        trunk = ChildRouteFactory.create(slug='foo')
        branch = RouteFactory.create(slug='branch', parent=trunk)
        leaf = RouteFactory.create(slug='leaf', parent=branch)

        new_trunk = ChildRouteFactory.create(slug='bar')
        branch.parent = new_trunk
        branch.save()

        leaf = Route.objects.get(pk=leaf.pk)
        self.assertEqual(leaf.url, '/bar/branch/leaf/')


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
        root = RootRouteFactory.create()
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
        leaf = RouteFactory.create(slug='leaf', parent=branch)

        with self.assertNumQueries(1):
            route = Route.objects.best_match_for_path('/branch/leaf/')

        self.assertEqual(route, leaf)

    def test_get_branch_with_leaf(self):
        """Check a Branch Route matches a path of its slug even if a Leaf exists."""
        branch = ChildRouteFactory.create(slug='branch')
        RouteFactory.create(slug='leaf', parent=branch)

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
        root = RootRouteFactory.create()

        with self.assertNumQueries(1):
            route = Route.objects.best_match_for_path('/absent-branch/')

        self.assertEqual(route, root)

    def test_fall_back_to_branch(self):
        """Check a Branch Route matches when no Leaf Route matches."""
        branch = ChildRouteFactory.create(slug='branch')

        with self.assertNumQueries(1):
            route = Route.objects.best_match_for_path('/branch/absent-leaf/')

        self.assertEqual(route, branch)


class RouteGetDescendantsTest(TestCase):
    """
    Test Route().get_descendants().

    All of these tests assert use of only one query:
        * Get the decendants of a Route:

            SELECT * FROM "routes_route"
            WHERE (
                NOT ("routes_route"."id" = <id>)
                AND "routes_route"."url"::text LIKE '<url>%'
            )
            ORDER BY "routes_route.url" DESC
    """
    def test_just_created(self):
        branch = RouteFactory.build()

        with self.assertNumQueries(0):
            # Descendants presumed nonsense as unsaved, so no query.
            descendants = list(branch.get_descendants())

        self.assertEqual(descendants, [])

    def test_no_descendants(self):
        branch = ChildRouteFactory.create()

        with self.assertNumQueries(1):
            descendants = list(branch.get_descendants())

        self.assertEqual(descendants, [])

    def test_descendants(self):
        branch = ChildRouteFactory.create()

        with self.assertNumQueries(1):
            descendants = list(branch.parent.get_descendants())

        self.assertEqual(descendants, [branch])


class RouteGetHandlerClassTest(TestCase):
    """Check the behaviour of Route().get_handler_class()."""
    def test_get_handler_class(self):
        """A Route's handler is looked up from the handler's path."""
        handler_class = handlers.BaseHandler
        route = RouteFactory.build()
        route.handler = handler_class.path()

        self.assertEqual(route.get_handler_class(), handler_class)


class RouteGetHandlerTest(TestCase):
    """Make sure that Route.get_handler acts as expected."""
    def test_get_handler(self):
        """We expect an instance of handler instanciated with a Route."""
        handler_class = handlers.BaseHandler
        route = RouteFactory.build()
        route.handler = handler_class.path()

        handler = route.get_handler()
        self.assertIsInstance(handler, handler_class)
        self.assertEqual(handler.route, route)

    def test_get_handler_again(self):
        """Make sure we always get the same instance of a handler on a Route."""
        handler_class = handlers.BaseHandler
        route = RouteFactory.build()
        route.handler = handler_class.path()

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
        route.get_handler_class = mock.MagicMock()
        request = mock.Mock()

        result = route.handle(request, '/branch/leaf/')

        expected = route.get_handler_class()(route).handle(request, '/leaf/')
        self.assertEqual(result, expected)


class RouteStrTest(TestCase):
    """Make sure that we get something nice when Route is cast to string."""
    def test_root_str(self):
        """A Root Route has a useful string representation."""
        route = RootRouteFactory.create()

        self.assertEqual(str(route), 'Route @ /')

    def test_child_str(self):
        """A Child Route has a string representation that includes its url."""
        leaf = ChildRouteFactory.create(slug='leaf')

        self.assertEqual(str(leaf), 'Route @ /leaf/')


class RouteCheckTest(TestCase):
    """Ensure that Route.check does useful validation."""
    def test_route_class(self):
        """The Route class does not require a handler attribute."""
        errors = Route.check()
        self.assertEqual(errors, [])

    def test_subclass_with_handler(self):
        """A subclass of Route must have a handler attribute."""
        class RouteWithHandler(Route):
            handler = 'has.been.set'

        errors = RouteWithHandler.check()
        self.assertEqual(errors, [])

    def test_subclass_without_handler(self):
        """A subclass of Route without a handler fails Route.check."""
        class RouteWithoutHandler(Route):
            pass  # handler not set

        errors = RouteWithoutHandler.check()
        self.assertEqual(len(errors), 1)
        error = errors[0]
        self.assertEqual(error.obj, RouteWithoutHandler)
        expected_msg = 'Route subclasses must have a `handler` attribute'
        self.assertEqual(error.msg, expected_msg)
