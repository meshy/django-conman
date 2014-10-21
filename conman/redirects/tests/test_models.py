from django.test import TestCase

from conman.routes.tests.test_models import NODE_BASE_FIELDS
from .factories import ChildNodeRedirectFactory
from ..models import NodeRedirect


class NodeRedirectTest(TestCase):
    def test_fields(self):
        """NodeRedirect has Node's fields and some specific to redirects."""
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
    """We should get something nice when RedirectNode is cast to string."""
    def test_str(self):
        """The str of a NodeRedirect identifies it by class and url."""
        leaf = ChildNodeRedirectFactory.create(slug='leaf')

        self.assertEqual(str(leaf), 'NodeRedirect @ /leaf/')
