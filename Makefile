SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make test | Run the tests."

test:
	@python -Wmodule -m coverage run ./conman/tests/run.py
	@coverage report --show-missing
	@flake8

release:
	python setup.py register sdist bdist_wheel upload
