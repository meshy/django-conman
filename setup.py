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
    install_requires=[],
)
