.PHONY: all export dependency install-hooks server dev test
#change it to your virtual env directory here
VENV=~/env

all: server

export:
	export VENV=$(VENV)

dependency:
	pip3 install -r requirements.txt

install-hooks: dependency
	pre-commit install -f --install-hooks

server: dependency install-hooks
	python3 -m tekinbot.tekin

dev: dependency install-hooks
	python3 -m tekinbot.tekin

test:
	python3 -m pytest tests/
