from django.test import TestCase

from conman.url_tree.tests.test_models import NODE_BASE_FIELDS
from .. import models


class PageTest(TestCase):
    def test_fields(self):
        """Check Page has Node's fields and a few of its own."""
        expected = (
            'id',
            'node_ptr',
            'node_ptr_id',
            'content',
        ) + NODE_BASE_FIELDS
        fields = models.Page._meta.get_all_field_names()
        self.assertCountEqual(fields, expected)
