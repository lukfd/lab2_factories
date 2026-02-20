IMAGE_NAME ?= lab2-fastapi
CONTAINER_NAME ?= lab2-fastapi
PORT ?= 8000
VENV ?= .venv
PYTHON ?= $(VENV)/bin/python
PIP ?= $(PYTHON) -m pip

.PHONY: venv activate install install-dev start docker-build docker-start docker-stop test test-no-container

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

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-start:
	docker run --rm -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):8000 \
		$(IMAGE_NAME)

docker-stop:
	docker stop $(CONTAINER_NAME)

test:
	$(PIP) install -e . --no-deps
	$(PYTHON) -m pytest tests -v

test-no-container:
	$(PIP) install -e . --no-deps
	$(PYTHON) -m pytest tests -v

