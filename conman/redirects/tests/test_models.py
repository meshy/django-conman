from django.test import TestCase

from ..models import NodeRedirect


class NodeRedirectTest(TestCase):
    def test_fields(self):
        expected = (
            'id',
            'node',
            'node_id',
            'target',
            'target_id',
        )
        fields = NodeRedirect._meta.get_all_field_names()
        self.assertCountEqual(fields, expected)
