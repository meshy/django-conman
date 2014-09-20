from django.test import TestCase

from .. import models
from conman.nav_tree.tests.test_models import NODE_BASE_FIELDS


class PageTest(TestCase):
    def test_fields(self):
        expected = (
            'id',
            'node_ptr',
            'node_ptr_id',
            'content',
        ) + NODE_BASE_FIELDS
        fields = models.Page._meta.get_all_field_names()
        self.assertCountEqual(fields, expected)
