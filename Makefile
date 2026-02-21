VENV ?= .venv
PYTHON ?= $(VENV)/bin/python
PIP ?= $(PYTHON) -m pip

.PHONY: venv activate install install-dev start test test-no-container

venv:
	python -m venv .venv

activate:
	. .venv/bin/activate

install:
	pip install -r requirements.txt

install-dev:
	pip install -e .[dev]

start:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	$(PIP) install -e . --no-deps
	$(PYTHON) -m pytest tests -v

