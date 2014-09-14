from django.test import TestCase

from .. import models


class NodeTest(TestCase):
    def test_fields(self):
        expected = (
            'id',
            'node',
            'node_id',
            'content',
        )
        fields = models.Page._meta.get_all_field_names()
        self.assertCountEqual(fields, expected)
