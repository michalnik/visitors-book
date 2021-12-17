.PHONY: all clean manage db-migrations db-migrate db-superuser run

SHELL := /bin/bash

# specify environment
ENVIRONMENT ?= development

# pip install options (target specific)
VENV_PIP_INSTALL_OPTION := -e .[devel]

# project directories
DIR_APP := visitors_book
DIR_ACCOUNT_MODELS := account
DIR_VISITS_RESTAURANTS_MODELS := visits_restaurants
DIR_ACCOUNT_MIGRATIONS := account/migrations
DIR_VISITS_RESTAURANTS_MIGRATIONS := visits_restaurants/migrations

# Python virtual environment location
VENV_NAME ?= venv
VENV_BIN := $(VENV_NAME)/bin

# Python virtual environment applications
PYTHON := $(VENV_BIN)/python3
DJANGO := $(PYTHON) -m django

# some other auxiliary variables
MIGRATIONS_ACCOUNT := $(shell ls $(DIR_ACCOUNT_MIGRATIONS)/*.py)
MIGRATIONS_VISITS_RESTAURANTS := $(shell ls $(DIR_VISITS_RESTAURANTS_MIGRATIONS)/*.py)
MODELS_ACCOUNT := $(DIR_ACCOUNT_MODELS)/models.py
MODELS_VISITS_RESTAURANTS := $(DIR_VISITS_RESTAURANTS_MODELS)/models.py

# which settings to use in CLI manage.py the script of Django
export PYTHONPATH := $(CURDIR)
export DJANGO_SETTINGS_MODULE := $(DIR_APP).settings.$(ENVIRONMENT)


all:
	@echo "make"
	@echo "    Print this help."
	@echo "make pre-install"
	@echo "    Install tools to create python virtual environment."
	@echo "make venv-python"
	@echo "    Install Python and Django requirements."
	@echo "make clean"
	@echo "    Cleans the project files from virtual environment"
	@echo "make manage"
	@echo "    It runs django-admin command. Other cli arguments can be passed via cli variable"
	@echo "    like this :"
	@echo "      make manage cli=\"shell\""
	@echo "        or"
	@echo "      make manage cli=\"migrate\""
	@echo "make run"
	@echo "    It runs Django development server on localhost at port 8000"
	@echo "make db-migrations"
	@echo "    It runs django-admin command - makemigrations. It creates"
	@echo "    migrations if it is needed."
	@echo "make db-migrate"
	@echo "    It runs django-admin command - migrate. It applies database migrations on"
	@echo "    database."


sql-lite-spatial: /tmp/visitors-book-sql-lite-spatial
/tmp/visitors-book-sql-lite-spatial:
	sudo apt install binutils libproj-dev gdal-bin libsqlite3-mod-spatialite
	touch /tmp/visitors-book-sql-lite-spatial

pre-install: sql-lite-spatial /tmp/visitors-book-pre-install
/tmp/visitors-book-pre-install:
	which python3 || sudo apt-get install -y python3
	which pip || sudo apt-get install -y python3-pip
	which virtualenv || sudo python3 -m pip install virtualenv
	touch /tmp/visitors-book-pre-install

venv-python: pre-install /tmp/visitors-book-venv-python
/tmp/visitors-book-venv-python: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	$(PYTHON) -m pip install -U pip setuptools
	$(PYTHON) -m pip install $(VENV_PIP_INSTALL_OPTION)
	touch /tmp/visitors-book-venv-python

clean:
	rm -f -v /tmp/visitors-book-*
	rm -rf -v $(VENV_NAME)
	rm -f -v $(DIR_APP)/db.sqlite3
	rm -f -v $(DIR_ACCOUNT_MIGRATIONS)/*.py
	rm -f -v $(DIR_VISITS_RESTAURANTS_MIGRATIONS)/*.py
	touch $(DIR_ACCOUNT_MIGRATIONS)/__init__.py
	touch $(DIR_VISITS_RESTAURANTS_MIGRATIONS)/__init__.py


run: venv-python
	$(DJANGO) runserver 127.0.0.1:8000

manage: venv-python
	$(DJANGO) $(cli);


db-migrations: venv-python $(MODELS_ACCOUNT) $(MODELS_VISITS_RESTAURANTS)
	$(DJANGO) makemigrations

db-migrate: venv-python $(MIGRATIONS_ACCOUNT) $(MIGRATIONS_VISITS_RESTAURANTS)
	$(DJANGO) migrate

db-superuser: venv-python
	$(DJANGO) createsuperuser
