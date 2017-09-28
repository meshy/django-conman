from django.contrib.admin import site
from django.test import TestCase

from conman.redirects.models import RouteRedirect, URLRedirect
from conman.routes.admin import RouteParentAdmin
from conman.routes.models import Route


class TestRouteParentAdminChildModels(TestCase):
    """Tests for RouteParentAdmin.get_child_models()."""
    def test_models_imported(self):
        """Each path in CONMAN_ADMIN_ROUTES is returned as a model."""
        admin = RouteParentAdmin(model=Route, admin_site=site)

        route_paths = ['redirects.RouteRedirect', 'redirects.URLRedirect']
        with self.settings(CONMAN_ADMIN_ROUTES=route_paths):
            models = admin.get_child_models()

        self.assertEqual(models, [RouteRedirect, URLRedirect])
