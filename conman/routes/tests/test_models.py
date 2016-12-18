from unittest import mock

from django.db.models import Manager
from django.db.utils import IntegrityError
from django.test import TestCase
from django.views.generic import View
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
            'mockviewroute',
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
        """Before object saved, avoid DB hits, and assume no descendants."""
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
        route = RouteFactory.create()

        self.assertEqual(str(route), 'Route @ /')

    def test_child_str(self):
        """A Child Route has a string representation that includes its url."""
        leaf = ChildRouteFactory.create(slug='leaf')

        self.assertEqual(str(leaf), 'Route @ /leaf/')


class RouteViewBindingTest(TestCase):
    """Views should not unexpectedly "bind" to Route subclasses."""
    def test_unbound_function(self):
        """Make sure that the handler is not bound to self on the view."""
        def unbound_function(request, **kwargs):
            return request

        class FunctionViewRoute(Route):
            view = unbound_function
            base_objects = Manager()

        route = FunctionViewRoute()
        request = mock.Mock()
        response = route.view(request)
        self.assertIs(response, request)

    def test_bound_function(self):
        """Make sure that class based views get the expected args."""
        class TestView(View):
            def dispatch(self, request, route=None):
                return self, request

        class ClassViewRoute(Route):
            view = TestView.as_view()
            base_objects = Manager()

        route = ClassViewRoute()
        request = mock.Mock()
        self_arg, request_arg = route.view(request)
        self.assertIsInstance(self_arg, TestView)
        self.assertIs(request_arg, request)
