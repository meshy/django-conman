from setuptools import setup


version = '0.0.1a1'

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
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    author='Charlie Denton',
    author_email='charlie@meshy.co.uk',
    url='https://github.com/meshy/django-conman/',
    install_requires=[
        'django-mptt>=0.7.4,<=0.8',
        'django-polymorphic-tree>=1.1,<2',
        'django-sirtrevor>=0.2.4,<0.3',
        'pillow>=2.9.0,<3',
    ],
)
