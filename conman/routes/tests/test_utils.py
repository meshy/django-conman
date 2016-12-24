from django.test import TestCase

from .. import utils


class TestSplitPath(TestCase):
    """Test the split_path util function."""
    def test_split_path(self):
        """split_path returns a list of all sub-paths of a url path."""
        paths = utils.split_path('/a/path/with/many/parts/')
        expected = [
            '/',
            '/a/',
            '/a/path/',
            '/a/path/with/',
            '/a/path/with/many/',
            '/a/path/with/many/parts/',
        ]
        self.assertEqual(paths, expected)

    def test_split_empty_path(self):
        """An empty path has sub-path '/'."""
        paths = utils.split_path('')
        expected = ['/']
        self.assertCountEqual(paths, expected)

    def test_split_root_path(self):
        """The root path '/' has sub-path '/'."""
        paths = utils.split_path('/')
        expected = ['/']
        self.assertCountEqual(paths, expected)

    def test_split_path_with_dots(self):
        """split_path does no special processing on a path containing dots."""
        paths = utils.split_path('/path/../')
        expected = [
            '/',
            '/path/',
            '/path/../',
        ]
        self.assertCountEqual(paths, expected)
