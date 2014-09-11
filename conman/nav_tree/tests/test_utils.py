from django.test import TestCase

from .. import utils


class TestSplitPath(TestCase):
    def test_split_path(self):
        paths = utils.split_path('/a/path/with/many/parts/')
        expected = [
            '/',
            '/a/',
            '/a/path/',
            '/a/path/with/',
            '/a/path/with/many/',
            '/a/path/with/many/parts/',
        ]
        self.assertCountEqual(paths, expected)  # Order does not matter

    def test_split_empty_path(self):
        paths = utils.split_path('')
        expected = ['/']
        self.assertCountEqual(paths, expected)

    def test_split_root_path(self):
        paths = utils.split_path('/')
        expected = ['/']
        self.assertCountEqual(paths, expected)

    def test_split_path_with_dots(self):
        paths = utils.split_path('/path/../')
        expected = [
            '/',
            '/path/',
            '/path/../',
        ]
        self.assertCountEqual(paths, expected)


class TestImportFromDottedPath(TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            utils.import_from_dotted_path('')

    def test_too_short(self):
        with self.assertRaises(ValueError):
            utils.import_from_dotted_path('antigravity')

    def test_import_module(self):
        result = utils.import_from_dotted_path('conman.nav_tree.utils')
        self.assertEqual(result, utils)

    def test_import_class(self):
        this_test = 'conman.nav_tree.tests.test_utils.TestImportFromDottedPath'
        result = utils.import_from_dotted_path(this_test)
        self.assertEqual(result, self.__class__)
