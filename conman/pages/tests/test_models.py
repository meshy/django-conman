from django.test import TestCase

from conman.routes.tests.test_models import NODE_BASE_FIELDS
from .. import models


class PageTest(TestCase):
    """Test the Page model."""
    def test_fields(self):
        """Check Page has Route's fields and a few of its own."""
        expected = (
            'id',
            'route_ptr',
            'route_ptr_id',
            'content',
        ) + NODE_BASE_FIELDS
        fields = models.Page._meta.get_all_field_names()
        self.assertCountEqual(fields, expected)
