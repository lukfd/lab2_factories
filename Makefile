venv:
	python -m venv .venv

activate:
	. .venv/bin/activate

install:
	pip install -r requirements.txt

start:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

