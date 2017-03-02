SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make test | Run the tests."

test:
	@python -Wmodule -m coverage run ./tests/run.py
	@coverage report --fail-under=100
	@flake8
	@isort --check

release:
	python setup.py register sdist bdist_wheel upload
