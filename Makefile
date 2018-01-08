VIRTUAL_ENV ?= .env
VIRTUALENV_DIR ?= $(VIRTUAL_ENV)
PYTHON = $(VIRTUALENV_DIR)/bin/python
PIP = $(VIRTUALENV_DIR)/bin/pip

create-virtualenv:
	virtualenv $(VIRTUALENV_DIR) --prompt="(flashlight-test-project)"

install-requirements:
	$(PIP) install -r requirements/requirements.txt

setup-dev: create-virtualenv install-requirements

run-client: create-virtualenv install-requirements
	$(PYTHON) ./client.py
