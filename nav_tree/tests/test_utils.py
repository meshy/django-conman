from django.test import TestCase

from .. import utils


class TestSplitPath(TestCase):
    def test_split_path(self):
        paths  = utils.split_path('/a/path/with/many/parts/')
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
        paths  = utils.split_path('')
        expected = ['/']
        self.assertCountEqual(paths, expected)

    def test_split_root_path(self):
        paths  = utils.split_path('/')
        expected = ['/']
        self.assertCountEqual(paths, expected)

    def test_split_path_with_dots(self):
        paths  = utils.split_path('/path/../')
        expected = [
            '/',
            '/path/',
            '/path/../',
        ]
        self.assertCountEqual(paths, expected)
