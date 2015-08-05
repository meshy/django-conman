import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = TEMPLATE_DEBUG = True


SECRET_KEY = 'example-app!'
ROOT_URLCONF = 'example.urls'
STATIC_URL = '/static/'


DATABASES = {'default': dj_database_url.config(
    default='postgres://localhost/conman_example',
)}
DATABASES['default']['ATOMIC_REQUESTS'] = True


INSTALLED_APPS = (
    'conman.routes',
    'conman.pages',
    'conman.redirects',

    'polymorphic',
    'polymorphic_tree',
    'sirtrevor',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
