from incuna_test_utils.testcases.request import BaseRequestTestCase

from .factories import UserFactory


class RequestTestCase(BaseRequestTestCase):
    """Add helper methods for working with requests in tests."""
    user_factory = UserFactory
