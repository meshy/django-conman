#! /usr/bin/env python
"""From http://stackoverflow.com/a/12260597/400691"""
import sys

from colour_runner.django_runner import ColourRunnerMixin
import dj_database_url
import django
from django.conf import settings
from django.test.runner import DiscoverRunner


settings.configure(
    DATABASES={
        'default': dj_database_url.config(default='postgres://localhost/conman'),
    },
    DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage',
    INSTALLED_APPS=(
        # Put contenttypes before auth to work around test issue.
        # See: https://code.djangoproject.com/ticket/10827#comment:12
        'django.contrib.sites',
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.admin',
        'conman.nav_tree',
        'conman.pages',
        'conman.redirects',
    ),
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',),
    SITE_ID = 1,
    ROOT_URLCONF='conman.nav_tree.urls',
    MIDDLEWARE_CLASSES=(),
    NAV_NODE_HANDLERS=(),
)

django.setup()


class TestRunner(ColourRunnerMixin, DiscoverRunner):
    pass


test_runner = TestRunner(verbosity=1)
failures = test_runner.run_tests(['conman'])
if failures:
    sys.exit(1)
