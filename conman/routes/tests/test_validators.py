from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Route
from ..validators import (
    validate_end_in_slash,
    validate_no_double_slashes,
    validate_no_hash_symbol,
    validate_no_questionmark,
    validate_start_in_slash,
)


class TestValidateEndInSlash(TestCase):
    """Tests for the validate_end_in_slash validator."""

    def test_no_ending_slash(self):
        """An ending slash is required."""
        path = '/must/end/with/a/slash'

        expected = 'Last character must be "/".'
        with self.assertRaisesMessage(ValidationError, expected):
            validate_end_in_slash(path)


class TestValidateStartInSlash(TestCase):
    """Tests for the validate_start_in_slash validator."""

    def test_no_starting_slash(self):
        """A starting slash is required."""
        path = 'must/start/with/a/slash/'

        expected = 'First character must be "/".'
        with self.assertRaisesMessage(ValidationError, expected):
            validate_start_in_slash(path)


class TestValidateNoQuestionmark(TestCase):
    """Tests for the validate_no_questionmark validator."""

    def test_has_questionmark(self):
        """A question mark is not acceptable."""
        path = '/is/this/ok?/absolutely/not/'

        expected = 'Question mark ("?") is not allowed.'
        with self.assertRaisesMessage(ValidationError, expected):
            validate_no_questionmark(path)


class TestValidateNoDoubleSlashes(TestCase):
    """Tests for the validate_no_double_slashes validator."""

    def test_has_double_slashes(self):
        """Two consecutive slashes is not acceptable."""
        path = '/is/this/ok//nope/'

        expected = 'Consecutive slashes ("//") are not allowed.'
        with self.assertRaisesMessage(ValidationError, expected):
            validate_no_double_slashes(path)


class TestValidateNoHashSymbol(TestCase):
    """Tests for the validate_no_hash_symbol validator."""

    def test_has_double_slashes(self):
        """A hash (pound) sign ("#") is not acceptable."""
        path = '/this/contains/a/#fragment/'

        expected = 'Hash symbol (AKA "pound", "#") is not allowed.'
        with self.assertRaisesMessage(ValidationError, expected):
            validate_no_hash_symbol(path)


class TestAllValidators(TestCase):
    """Tests all validators."""
    validators = [
        validate_end_in_slash,
        validate_start_in_slash,
        validate_no_double_slashes,
        validate_no_hash_symbol,
        validate_no_questionmark,
    ]

    def test_root(self):
        """A root url ("/") doesn't raise an error."""
        path = '/'
        for validator in self.validators:
            with self.subTest(validator=validator):
                self.assertIsNone(validator(path))

    def test_ok(self):
        """A standard url doesn't raise an error."""
        path = '/a/path/that/is/a-ok/'
        for validator in self.validators:
            with self.subTest(validator=validator):
                self.assertIsNone(validator(path))

    def test_integration(self):
        """Ensure these validators are installed on Route.url."""
        field_validators = Route._meta.get_field('url').validators
        for validator in self.validators:
            with self.subTest(validator=validator):
                self.assertIn(validator, field_validators)
