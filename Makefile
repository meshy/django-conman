SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make test | Run the tests."

test:
	@coverage run ./conman/tests/run.py
	@coverage report --fail-under=100
	@flake8

release:
	python setup.py register sdist bdist_wheel upload
