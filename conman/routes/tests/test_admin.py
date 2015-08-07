from incuna_test_utils.testcases.integration import BaseAdminIntegrationTestCase

from conman.tests.factories import AdminFactory
from .factories import RootRouteFactory
from ..models import Route


class TestRouteAdmin(BaseAdminIntegrationTestCase):
    """Test the functionality of the Route admin."""
    user_factory = AdminFactory
    model = Route

    def test_add_page(self):
        """Ensure the add page is accessible."""
        response = self.get_admin_add_page()
        self.assertEqual(response.status_code, 200)

    def test_changelist_page(self):
        """Ensure the list page is accessible."""
        response = self.get_admin_changelist_page()
        self.assertEqual(response.status_code, 200)

    def test_change_page(self):
        """Ensure the update page is accessible."""
        route = RootRouteFactory.create()
        response = self.get_admin_change_page(route)
        self.assertEqual(response.status_code, 200)

    def test_delete_page(self):
        """Ensure the delete page is accessible."""
        route = RootRouteFactory.create()
        response = self.get_admin_delete_page(route)
        self.assertEqual(response.status_code, 200)
