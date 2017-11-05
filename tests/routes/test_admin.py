from django.contrib.admin import site
from django.contrib.admin.widgets import AdminTextInputWidget
from django.test import mock, SimpleTestCase, TestCase

from conman.routes.admin import RouteParentAdmin
from conman.routes.models import Route


class TestRouteParentAdminChildModels(TestCase):
    """Tests for RouteParentAdmin.get_child_models()."""
    def test_delegation(self):
        """Fetching subclasses is delegated to Route.get_subclasses()."""
        admin = RouteParentAdmin(model=Route, admin_site=site)

        with mock.patch.object(Route, 'get_subclasses') as get_subclasses:
            get_subclasses.return_value = (c for c in [Route])
            subclasses = admin.get_child_models()

        self.assertIsInstance(subclasses, list)
        get_subclasses.assert_called_with()


class TestRouteURLWidget(SimpleTestCase):
    """Test the widget used for Route.url in the admin."""
    def test_widget(self):
        """Route.url uses a single-line widget in the admin."""
        admin = RouteParentAdmin(model=Route, admin_site=site)
        db_field = Route._meta.get_field('url')
        form_field = admin.formfield_for_dbfield(db_field, request=mock.Mock())
        self.assertIsInstance(form_field.widget, AdminTextInputWidget)
