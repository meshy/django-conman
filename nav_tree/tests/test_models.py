from django.test import TestCase

from .. import models
from . import factories


class NodeTest(TestCase):
    def test_fields(self):
        expected = (
            'id',
            'parent',
            'parent_id',
            'slug',
            'url',

            # MPTT fields
            'level',
            'lft',
            'rght',
            'tree_id',

            # Incoming foreign keys
            'children',  # FK from self. The other end of "parent".
        )
        fields = models.Node._meta.get_all_field_names()
        self.assertCountEqual(fields, expected)


class NodeValidateOnSave(TestCase):
    def test_create_root_with_slug(self):
        """Root must not have a slug"""
        root_node = factories.NodeFactory.build(slug='slug', parent=None)

        with self.assertRaises(ValueError):
            root_node.save()

    def test_create_leaf_without_slug(self):
        """Leaf nodes must have a slug"""
        root_node = factories.NodeFactory.create(slug='', parent=None)
        leaf = factories.NodeFactory.build(slug='', parent=root_node)

        with self.assertRaises(ValueError):
            leaf.save()


class NodeCachesURLOnCreateTest(TestCase):
    def setUp(self):
        self.root = factories.NodeFactory.create(slug='', parent=None)

    def test_create_root(self):
        """Root node should be at the root url."""
        self.assertEqual(self.root.url, '/')

    def test_create_leaf_on_root(self):
        """Children of the root should be at /<slug>/."""
        leaf = factories.NodeFactory.create(slug='leaf', parent=self.root)

        self.assertEqual(leaf.url, '/leaf/')

    def test_create_child_of_child(self):
        """Children of children should be at /<parent-slug>/<slug>/."""
        branch = factories.NodeFactory.create(slug='branch', parent=self.root)
        leaf = factories.NodeFactory.create(slug='leaf', parent=branch)

        self.assertEqual(leaf.url, '/branch/leaf/')


class NodeCachesURLOnRenameTest(TestCase):
    def setUp(self):
        self.root = factories.NodeFactory.create(slug='', parent=None)

    def test_rename_leaf(self):
        """Changing slug on a leaf should update the cached url."""
        leaf = factories.NodeFactory.create(slug='foo', parent=self.root)

        leaf.slug = 'bar'
        leaf.save()

        self.assertEqual(leaf.url, '/bar/')

    def test_rename_branch(self):
        """Changing a branch slug should update the child url."""
        branch = factories.NodeFactory.create(slug='foo', parent=self.root)
        leaf = factories.NodeFactory.create(slug='leaf', parent=branch)

        branch.slug = 'bar'
        branch.save()

        leaf = models.Node.objects.get(pk=leaf.pk)
        self.assertEqual(leaf.url, '/bar/leaf/')

    def test_rename_trunk(self):
        """Changing a trunk slug should update the grandchild url."""
        trunk = factories.NodeFactory.create(slug='foo', parent=self.root)
        branch = factories.NodeFactory.create(slug='branch', parent=trunk)
        leaf = factories.NodeFactory.create(slug='leaf', parent=branch)

        trunk.slug = 'bar'
        trunk.save()

        leaf = models.Node.objects.get(pk=leaf.pk)
        self.assertEqual(leaf.url, '/bar/branch/leaf/')


class NodeCachesURLOnMoveTest(TestCase):
    def setUp(self):
        self.root = factories.NodeFactory.create(slug='', parent=None)

    def test_move_leaf(self):
        """Moving a leaf onto a new branch should update the cached url."""
        branch = factories.NodeFactory.create(slug='foo', parent=self.root)
        leaf = factories.NodeFactory.create(slug='leaf', parent=branch)

        new_branch = factories.NodeFactory.create(slug='bar', parent=self.root)
        leaf.parent = new_branch
        leaf.save()

        self.assertEqual(leaf.url, '/bar/leaf/')

    def test_move_branch(self):
        """Moving a branch onto a new trunk should update the leaf urls."""
        trunk = factories.NodeFactory.create(slug='foo', parent=self.root)
        branch = factories.NodeFactory.create(slug='branch', parent=trunk)
        leaf = factories.NodeFactory.create(slug='leaf', parent=branch)

        new_trunk = factories.NodeFactory.create(slug='bar', parent=self.root)
        branch.parent = new_trunk
        branch.save()

        leaf = models.Node.objects.get(pk=leaf.pk)
        self.assertEqual(leaf.url, '/bar/branch/leaf/')



