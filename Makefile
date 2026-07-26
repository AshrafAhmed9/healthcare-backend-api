.PHONY: up down migrate test lint format seed

up:
	docker compose up --build

down:
	docker compose down -v

migrate:
	python manage.py migrate

test:
	pytest --cov --cov-report=term-missing --cov-fail-under=90

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .

seed:
	python manage.py seed_demo
