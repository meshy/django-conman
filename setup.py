from setuptools import setup, find_packages


version = '0.0.1'

setup(
    name='django-conman',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    description='A modular CMS for django, sponsored by Incuna',
    author='Charlie Denton',
    author_email='charlie@meshy.co.uk',
    url='https://github.com/meshy/django-conman/',
    install_requires=[
        'django-mptt>=0.6.1,<=0.7',
        'django-sirtrevor==0.2.3',
    ],
)
