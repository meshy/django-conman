from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.test import TestCase
from incuna_test_utils.utils import field_names

from conman.routes.tests.test_models import NODE_BASE_FIELDS
from .factories import ChildRouteRedirectFactory
from ..models import RouteRedirect, URLRedirect
from ..views import RouteRedirectView


class RouteRedirectTest(TestCase):
    """Test the RouteRedirect model."""
    def test_fields(self):
        """RouteRedirect has Route's fields and some specific to redirects."""
        expected = (
            'id',
            'route_ptr',
            'target',
            'permanent',
        ) + NODE_BASE_FIELDS
        fields = field_names(RouteRedirect)
        self.assertCountEqual(fields, expected)

    def test_target_self(self):
        """A RouteRedirect's target cannot be itself."""
        redirect = ChildRouteRedirectFactory.create()

        redirect.target = redirect

        with self.assertRaises(ValidationError):
            redirect.save()

    def test_target_self_with_form(self):
        """A form for RouteRedirect is invalid if its target is itself."""
        class RouteRedirectForm(ModelForm):
            class Meta:
                model = RouteRedirect
                exclude = []

        redirect = ChildRouteRedirectFactory.create()

        data = {'target': redirect.pk}
        form = RouteRedirectForm(data, instance=redirect)
        form.is_valid()

        self.assertIn('target', form.errors)


class RouteRedirectViewTest(TestCase):
    """Test RouteRedirect.view."""
    def test_view(self):
        """RouteRedirect uses the RouteRedirectView."""
        view = RouteRedirect.view
        expected = RouteRedirectView.as_view()

        self.assertEqual(view.__name__, expected.__name__)
        self.assertEqual(view.__module__, expected.__module__)


class RouteRedirectUnicodeMethodTest(TestCase):
    """We should get something nice when RedirectRoute is cast to string."""
    def test_str(self):
        """The str of a RouteRedirect identifies it by class and url."""
        leaf = ChildRouteRedirectFactory.create(slug='leaf')

        self.assertEqual(str(leaf), 'RouteRedirect @ /leaf/')


class URLRedirectTest(TestCase):
    """Test the URLRedirect model."""
    def test_fields(self):
        """URLRedirect has Route's fields and some specific to redirects."""
        expected = (
            'id',
            'route_ptr',
            'target',
            'permanent',
        ) + NODE_BASE_FIELDS
        fields = field_names(URLRedirect)
        self.assertCountEqual(fields, expected)
