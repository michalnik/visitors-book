
.PHONY: all clean run shell lint tests django-test python-coverage

SHELL := /bin/bash

# specify environment
export ENVIRONMENT ?= development

# project directories
DIR_APP := visitors_book
DIR_ACCOUNT_MODELS := account
DIR_VISITS_RESTAURANTS_MODELS := visits_restaurants
DIR_ACCOUNT_MIGRATIONS := account/migrations
DIR_VISITS_RESTAURANTS_MIGRATIONS := visits_restaurants/migrations
DIR_ACCOUNT_FIXTURES := account/fixtures
DIR_VISITS_RESTAURANTS_FIXTURES := visits_restaurants/fixtures

# some other auxiliary variables
MIGRATIONS_ACCOUNT := $(shell ls $(DIR_ACCOUNT_MIGRATIONS)/*.py)
MIGRATIONS_VISITS_RESTAURANTS := $(shell ls $(DIR_VISITS_RESTAURANTS_MIGRATIONS)/*.py)
MODELS_ACCOUNT := $(DIR_ACCOUNT_MODELS)/models.py
MODELS_VISITS_RESTAURANTS := $(DIR_VISITS_RESTAURANTS_MODELS)/models.py
FIXTURES_ACCOUNT := $(shell ls $(DIR_ACCOUNT_FIXTURES))
FIXTURES_VISITS_RESTAURANTS := $(shell ls $(DIR_VISITS_RESTAURANTS_FIXTURES))
FIXTURE_ACCOUNT_FILES := $(shell for fixture in $(FIXTURES_ACCOUNT); do echo "$(DIR_ACCOUNT_FIXTURES)/$$fixture"; done)
FIXTURE_VISITS_RESTAURANTS_FILES := $(shell for fixture in $(FIXTURES_VISITS_RESTAURANTS); do echo "$(DIR_VISITS_RESTAURANTS_FIXTURES)/$$fixture"; done)

# docker container names
CON_NMS := visitorsbook_db_1 visitorsbook_api_1

all:
	@echo "make"
	@echo "    Print this help."
	@echo "make clean"
	@echo "    It cleans the project files from database migrations and docker things and others..."
	@echo "make makemigrations"
	@echo "    It calls django-admin makemigrations."
	@echo "make migrate"
	@echo "    It calls django-admin migrate."
	@echo "make run"
	@echo "    It runs Django development server at port 8000."
	@echo "make loadfixtures"
	@echo "    It load fixtures into database to have some tests data in it."
	@echo "make shell"
	@echo "    It runs django-admin shell command to inspect database models or code ..."
	@echo "make tests"
	@echo "    It runs django-admin test command with coverage report."
	@echo "make lint"
	@echo "    It runs linting of source code with pylint."


clean:
	rm -f -v /tmp/visitors-book-*
	rm -f -v $(DIR_ACCOUNT_MIGRATIONS)/*.py
	rm -f -v $(DIR_VISITS_RESTAURANTS_MIGRATIONS)/*.py
	touch $(DIR_ACCOUNT_MIGRATIONS)/__init__.py
	touch $(DIR_VISITS_RESTAURANTS_MIGRATIONS)/__init__.py
	sudo docker stop $(CON_NMS) || echo "cannot stop docker container"
	sudo docker rm $(CON_NMS) || echo "cannot remove docker container"
	sudo docker rmi visitor:latest || echo "cannot remove docker image"


build-visitor-latest: /tmp/visitors-book-docker-image
/tmp/visitors-book-docker-image:
	sudo docker build --no-cache --build-arg ENVIRONMENT=$(ENVIRONMENT) -t visitor:latest .
	touch /tmp/visitors-book-docker-image
makemigrations: build-visitor-latest $(MODELS_ACCOUNT) $(MODELS_VISITS_RESTAURANTS) /tmp/visitors-book-makemigrations
/tmp/visitors-book-makemigrations:
	sudo -E docker-compose run api makemigrations
	touch /tmp/visitors-book-makemigrations
migrate: makemigrations $(MIGRATIONS_ACCOUNT) $(MIGRATIONS_VISITS_RESTAURANTS) /tmp/visitors-book-migrate
/tmp/visitors-book-migrate:
	sudo -E docker-compose run api migrate
	touch /tmp/visitors-book-migrate
loadfixtures: migrate /tmp/visitors-book-load-fixtures
/tmp/visitors-book-load-fixtures:
	sudo -E docker-compose run api loaddata $(FIXTURE_ACCOUNT_FILES) $(FIXTURE_VISITS_RESTAURANTS_FILES)
	touch /tmp/visitors-book-load-fixtures


tests: django-test python-coverage
django-test:
	sudo -E docker-compose run --entrypoint 'python -m coverage' api run \
--source="visits_restaurants" manage.py test
python-coverage:
	sudo -E docker-compose run --entrypoint 'python -m coverage' api report


lint:
	sudo -E docker-compose run --entrypoint 'python -m pylint' api --rcfile=pylintrc \
account visitors_book visits_restaurants


run: migrate
	sudo -E docker-compose up api


shell: migrate
	sudo -E docker-compose run api shell
