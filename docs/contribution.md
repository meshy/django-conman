# Contribution

You can find the [source code for django-conman][github-repo] on github.

We gratefully welcome contributions, be they bug reports, code, reviews,
documentation, or any other constructive assistance.

## Tests

In order to help keep the code reliable we automatically run a test suite
against the changes whenever a commit is pushed to the github repo.

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

1. The tests assume you're running [PostgresQL locally without a
   password][postgres-without-passwords]. If you need to override this, you can
   set the `DATABASE_URL` environment variable as accepted by
   [dj-database-url][dj-database-url].

1. Finally, you should be able to run the tests with:

        make test

!!! Note
    There is one minor difference between local tests and those run against
    pull-requests: we do not enforce the errors thrown by
    [flake8-docstrings][flake8-docstrings], we only run the check locally to
    encourage thorough documentation.


## Code style

Hopefully, adherence to a code style will keep our codebase in good shape for
as long as possible.

!!! Note
    We endeavour to avoid use of `#noqa` or other methods of dodging the code
    quality checks, and we're keen to retain our 100% test coverage. Apologies
    if this appears to be a little draconian.

### Python

Python code should adhere to [PEP8][pep8]. We also have a couple of other
eccentricities. Please:

- Try to stick to the "max 80 chars per line" rule. We have some flexibility,
  but our linter will start to complain at 90 chars. If you're going over that,
  there's probably a nicer way to structure the logic. Do not wrap long lines
  with `\` (backslash).

- Make multi-line lists have one element per line, and a trailing comma. Indent
  the elements by four spaces instead of aligning with the brace.

        nice_things = [
            'long lists with one element per line',
            'four space indents',
            'trailing commas',
        ]

- Keep imports in order: future, core library, 3rd party, 1st party, then
  relative. Rather than bother to do this by hand, we recommend [isort][isort].

- When in doubt, keep things in alphabetical order.

### Automation

As well as running continuous integration tests, we automate the process
of checking adherence to our style guide where possible.

There are a couple of tools we recommend to make things easier:

- [EditorConfig][editorconfig]: This helps to normalise simple issues like
  how many spaces constitute a tab, clearing whitespace at the end of lines,
  and missing newlines at the end of files. Most people should find there is a
  plugin for their editor.

- [isort][isort]: This simplifies the process of keeping the imports in order.
  To automatically sort all imports before committing, run `isort --apply`.
  There are a number of editor plugins available, if you prefer.


[dj-database-url]: https://github.com/kennethreitz/dj-database-url
[editorconfig]: http://editorconfig.org/
[flake8-docstrings]: https://pypi.python.org/pypi/flake8-docstrings
[github-repo]: https://github.com/meshy/django-conman
[isort]: https://github.com/timothycrosley/isort
[pep8]: https://www.python.org/dev/peps/pep-0008/
[postgres-without-passwords]: http://meshy.co.uk/posts/postgresql-without-passwords
[virtualenvwrapper]: https://pypi.python.org/pypi/virtualenvwrapper
