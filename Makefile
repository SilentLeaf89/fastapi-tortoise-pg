COMPOSE = docker compose

build:
	$(COMPOSE) build

dev:
	$(COMPOSE) -f docker-compose.yml -f docker-compose.override.dev.yml up -d

logs:
	$(COMPOSE) logs --follow

stop:
	$(COMPOSE) down

remove:
	$(COMPOSE) down --remove-orphans

test:
	$(COMPOSE) -f docker-compose.yml -f docker-compose.override.dev.yml -f docker-compose.override.tests.yml up -d --force-recreate
