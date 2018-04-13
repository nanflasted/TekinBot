.PHONY: all

all: venv

clean:
	rm -f .activate.sh
	rm -f .deactivate.sh
	rm -rf ./venv

venv:
	python3 -m venv ./venv
	echo "deactivate" > .deactivate.sh
	chmod 700 .deactivate.sh
	ln -s ./venv/bin/activate .activate.sh
	./venv/bin/pip install -r requirements-dev.txt

install-hooks:
	pre-commit install -f --install-hooks

server: install-hooks
	./venv/bin/pip install -r requirements.txt
	python3 -m tekinbot.tekin

dev: install-hooks
	python3 -m tekinbot.tekin --dry-run --no-db

test:
	python3 -m pytest tests/
