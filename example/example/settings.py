import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = True


SECRET_KEY = 'example-app!'
ROOT_URLCONF = 'example.urls'
STATIC_URL = '/static/'


DATABASES = {'default': dj_database_url.config(
    default='postgres://localhost/conman_example',
)}
DATABASES['default']['ATOMIC_REQUESTS'] = True


INSTALLED_APPS = (
    'conman.routes',
    'conman.redirects',

    'polymorphic',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)


MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': False,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
        'debug': DEBUG,
        'loaders': [
            'django.template.loaders.app_directories.Loader',
        ],
    },
}]
