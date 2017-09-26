# Contribution

You can find the [source code for django-conman][github-repo] on github.

We gratefully welcome contributions, be they bug reports, code, reviews,
documentation, or any other constructive assistance.

## Tests

In order to help keep the code reliable we automatically run a test suite
against the changes whenever a commit is pushed to the github repo. As well as
behavioural tests, we try to automate the process of checking adherence to our
style guide.

Where possible, we endeavour to avoid use of `#noqa` or other methods of dodging
code quality checks, and we're keen to retain our 100% test coverage.

!!! Note
    For your convenience, it's probably a good idea to run the tests locally
    before submitting a pull request for approval. The tests can be run locally
    in a few seconds, but it can take minutes for the results to show up on
    github. This may save you a lot of bother if/when they fail. If you're
    having issues getting the tests to pass, submit the PR, and we may be able
    to help.


### Local testing

The test suite depends on Python 3 and expects PostgresQL. To run the tests
locally:

1. Clone the git repo:

        git clone git@github.com:meshy/django-conman.git

1. Set up a python virtual environment (we recommend
   [virtualenvwrapper][virtualenvwrapper]) and install the required python
   packages:

        cd django-conman
        mkvirtualenv django-conman -p $(which python3)
        pip install -r requirements.txt

1. The tests assume you're running PostgresQL locally without a password. If you
   need to override this, you can set the `DATABASE_URL` environment variable
   as accepted by [dj-database-url][dj-database-url].

1. Finally, you should be able to run the tests with:

        make test

!!! Note
    There is one minor difference between local tests and those run against
    pull-requests: we do not enforce the errors thrown by
    [flake8-docstrings][flake8-docstrings], we only run the check locally to
    encourage thorough documentation.


[dj-database-url]: https://github.com/kennethreitz/dj-database-url
[flake8-docstrings]: https://pypi.python.org/pypi/flake8-docstrings
[github-repo]: https://github.com/meshy/django-conman
[virtualenvwrapper]: https://pypi.python.org/pypi/virtualenvwrapper
