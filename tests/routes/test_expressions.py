from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from conman.routes.expressions import CharCount
from conman.routes.models import Route

from .factories import RouteFactory


class TestCharCount(TestCase):
    """Tests for CharCount."""
    def test_query(self):
        """Match the exact value of the generated query."""
        with CaptureQueriesContext(connection):
            # The "only" here is handy to keep the query as short as possible.
            list(Route.objects.only('id').annotate(level=CharCount('url', char='/')))
        # Excuse the line wrapping here -- I wasn't sure of a nice way to do it.
        # I decided it was better to just keep it simple.
        expected = (
            'SELECT "routes_route"."id", ' +
            'CHAR_LENGTH("routes_route"."url") - ' +
            '''CHAR_LENGTH(REPLACE("routes_route"."url", '/', '')) AS "level" ''' +
            'FROM "routes_route"'
        )
        self.assertEqual(connection.queries[0]['sql'], expected)

    def test_annotation(self):
        """Test the expression can be used for annotation."""
        RouteFactory.create(url='/fifth/level/zero/indexed/path/')
        route = Route.objects.annotate(level=CharCount('url', char='/')).get()
        # The number of "/" in the path minus one for zero-indexing.
        self.assertEqual(route.level, 5)

    def test_calling_format(self):
        """Ensure the 'char' argument is always a keyword-arg."""
        with self.assertRaises(TypeError):
            CharCount('url', 'a')

    def test_char_length(self):
        """Ensure 'char' length is always 1."""
        msg = 'CharCount must count exactly one char.'
        for not_a_char in ['', 'no']:
            with self.subTest(char=not_a_char):
                with self.assertRaisesMessage(ValueError, msg):
                    CharCount('url', char=not_a_char)
