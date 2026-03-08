.PHONY: up down build logs migrate shell-backend shell-db

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

migrate:
	docker compose exec backend alembic upgrade head

shell-backend:
	docker compose exec backend bash

shell-db:
	docker compose exec db psql -U postgres -d productivity
