# Auto-detect Docker Compose command: V2 plugin ("docker compose") or V1 standalone ("docker-compose")
DOCKER_COMPOSE := $(shell docker compose version > /dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

.PHONY: up down build logs migrate shell-backend shell-db

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

build:
	$(DOCKER_COMPOSE) build

logs:
	$(DOCKER_COMPOSE) logs -f

migrate:
	$(DOCKER_COMPOSE) exec backend alembic upgrade head

shell-backend:
	$(DOCKER_COMPOSE) exec backend bash

shell-db:
	$(DOCKER_COMPOSE) exec db psql -U postgres -d productivity
