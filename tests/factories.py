import factory
from django.conf import settings


class UserFactory(factory.DjangoModelFactory):
    """Create instances of User for testing."""
    class Meta:
        model = settings.AUTH_USER_MODEL
