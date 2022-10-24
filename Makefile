##########################################################################
# This is the project's makefile.
#
# You can build, test, setup fixtures, start, stop, export, run commands, etc.
##########################################################################

##########################################################################
# VARIABLES
##########################################################################
TAG := $(shell date "+%Y%m%d-%H%m")

##########################################################################
# MENU
##########################################################################
.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##########################################################################
# START / STOP
##########################################################################
.PHONY: migration
migration: # migration
	python manage.py makemigrations && \
	python manage.py migrate

.PHONY: run
run: # run dev server (wsgi only) locally
	make migration && \
	python manage.py runserver

.PHONY: install
install: # install dependencies
	pip-compile -U && \
	pip install -r requirements.txt

.PHONY: init
init: # initialize
	virtualenv venv && \
	venv\scripts\activate && \
	pip install pip-tools && \

##########################################################################
# BACKEND
##########################################################################
.PHONY: test
test: # runs all tests for backend
	python manage.py test --failfast --no-input --keepdb -v 2
