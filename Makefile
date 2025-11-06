.PHONY: dev lint format test cov migrate superuser

dev:
	python manage.py runserver

migrate:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

lint:
	flake8
	isort --check-only .
	black --check .
	djlint templates --check --quiet || true

format:
	isort .
	black .
	djlint templates --reformat --quiet || true

test:
	pytest

cov:
	pytest --cov=carelink --cov-report=term-missing

