from setuptools import setup, find_packages


version = '0.0.1'

setup(
    name='django-conman',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    description='A modular CMS for django',
    author='Incuna',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/django-conman/',
    install_requires=[
        'django-mptt>=0.6.1,<=0.7',
        'django-polymorphic-tree>=1.0b1',
        'django-sirtrevor>=0.2.3,<0.3',
    ],
)
