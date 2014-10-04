SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make test | Run the tests."

test:
	@coverage run ./conman/tests/run.py
	@coverage report --show-missing
	@flake8 . --application-import-names=conman --import-order-style=google

release:
	python setup.py register sdist bdist_wheel upload
