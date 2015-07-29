from django.test import TestCase
from incuna_test_utils.utils import field_names

from conman.routes.tests.test_models import NODE_BASE_FIELDS
from .. import models


class PageTest(TestCase):
    """Test the Page model."""
    def test_fields(self):
        """Check Page has Route's fields and a few of its own."""
        expected = (
            'id',
            'route_ptr',
            'content',
        ) + NODE_BASE_FIELDS
        fields = field_names(models.Page)
        self.assertCountEqual(fields, expected)
