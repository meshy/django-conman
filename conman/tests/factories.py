import factory
from django.conf import settings


class UserFactory(factory.DjangoModelFactory):
    """Create instances of User for testing."""
    class Meta:
        model = settings.AUTH_USER_MODEL

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set and store a password for access in tests."""
        self.raw_password = 'default_password' if extracted is None else extracted
        self.set_password(self.raw_password)
        if create:
            self.save()


class AdminFactory(UserFactory):
    is_staff = True
    is_superuser = True
