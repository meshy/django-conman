import sys

from setuptools import setup


if sys.version_info <= (3, 4):
    msg = 'Minimum python version requirement not met.'
    raise EnvironmentError(msg)


version = '0.1.0'


setup(
    name='django-conman',
    packages=['conman'],
    include_package_data=True,
    version=version,
    description='A modular CMS for django, sponsored by Incuna',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    author='Charlie Denton',
    author_email='charlie@meshy.co.uk',
    url='https://github.com/meshy/django-conman/',
    install_requires=[
        'django-polymorphic~=1.2.0',
    ],
)
