SHELL := /bin/bash

RED := \033[0;31m
GREEN := \033[0;32m
PURPLE := \033[1;35m
RESET := \033[0m
FAILURE := (echo -e "${RED}FAILURE${RESET}" && exit 1)
SUCCESS := echo -e "${GREEN}SUCCESS${RESET}"
RESULT := && ${SUCCESS} || ${FAILURE}

help:
	@echo "Usage:"
	@echo " make test | Run the tests."

test:
	@echo -e "${PURPLE}Run tests:${RESET}"
	@python -Wmodule -m coverage run ./tests/run.py ${RESULT}
	@echo -e "\n${PURPLE}Check for untested code:${RESET}"
	@coverage report --fail-under=100 ${RESULT}
	@echo -e "\n${PURPLE}Check for flake8 violations:${RESET}"
	@flake8 ${RESULT}
	@echo -e "\n${PURPLE}Check for unsorted imports:${RESET}"
	@isort --check ${RESULT}
	@echo -e "\n${PURPLE}Check for missing migrations:${RESET}"
	@example/manage.py makemigrations --check --dry-run ${RESULT}

release:
	python setup.py sdist bdist_wheel
	twine upload dist/* -s
