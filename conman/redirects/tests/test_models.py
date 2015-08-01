from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.test import TestCase

from conman.routes.tests.test_models import NODE_BASE_FIELDS
from .factories import ChildRouteRedirectFactory
from ..models import RouteRedirect


class RouteRedirectTest(TestCase):
    """Test the RouteRedirect model."""
    def test_fields(self):
        """RouteRedirect has Route's fields and some specific to redirects."""
        expected = (
            'id',
            'route_ptr',
            'route_ptr_id',
            'target',
            'target_id',
            'permanent',
        ) + NODE_BASE_FIELDS
        fields = RouteRedirect._meta.get_all_field_names()
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


class RouteRedirectUnicodeMethodTest(TestCase):
    """We should get something nice when RedirectRoute is cast to string."""
    def test_str(self):
        """The str of a RouteRedirect identifies it by class and url."""
        leaf = ChildRouteRedirectFactory.create(slug='leaf')

        self.assertEqual(str(leaf), 'RouteRedirect @ /leaf/')
