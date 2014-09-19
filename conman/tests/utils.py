from incuna_test_utils.testcases.integration import BaseIntegrationTestCase
from incuna_test_utils.testcases.request import BaseRequestTestCase

from .factories import UserFactory


class RequestTestCase(BaseRequestTestCase):
    user_factory = UserFactory


class IntegrationTestCase(BaseIntegrationTestCase):
    user_factory = UserFactory
