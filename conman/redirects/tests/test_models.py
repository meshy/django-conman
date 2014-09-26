from django.test import TestCase

from ..models import NodeRedirect
from .factories import ChildNodeRedirectFactory
from conman.nav_tree.tests.factories import RootNodeFactory
from conman.nav_tree.tests.test_models import NODE_BASE_FIELDS


class NodeRedirectTest(TestCase):
    def test_fields(self):
        expected = (
            'id',
            'node_ptr',
            'node_ptr_id',
            'target',
            'target_id',
            'permanent',
        ) + NODE_BASE_FIELDS
        fields = NodeRedirect._meta.get_all_field_names()
        self.assertCountEqual(fields, expected)


class NodeRedirectUnicodeMethodTest(TestCase):
    """We should get something nice when RedirectNode is cast to string"""
    def test_str(self):
        leaf = ChildNodeRedirectFactory.create(slug='leaf')

        self.assertEqual(str(leaf), 'NodeRedirect @ /leaf/')
