from django.db import IntegrityError
from django.test import TestCase

from .. import models
from . import factories


class PageTest(TestCase):
    def test_fields(self):
        expected = (
            'id',
            'node',
            'node_id',
            'content',
        )
        fields = models.Page._meta.get_all_field_names()
        self.assertCountEqual(fields, expected)


class TestPageNodeUniqueness(TestCase):
    def test_two_pages_on_a_node(self):
        page = factories.PageFactory()

        with self.assertRaises(IntegrityError):
            factories.PageFactory(node=page.node)
