.DEFAULT_GOAL := run

.PHONY: up bootstrap run format-check docformat-check lint type-check complexity dead-code security test test-unit test-integration status reset down

up:
	docker compose up -d --wait postgres minio

bootstrap: up
	docker compose run --rm --no-deps minio-init

run: bootstrap
	docker compose run --rm --no-deps --build pipeline

format-check:
	docker compose run --rm --no-deps --build pipeline ruff format --check .

docformat-check:
	docker compose run --rm --no-deps --build pipeline pydocstringformatter --exit-code --quiet .

lint:
	docker compose run --rm --no-deps --build pipeline ruff check .

type-check:
	docker compose run --rm --no-deps --build pipeline mypy .

complexity:
	docker compose run --rm --no-deps --build pipeline radon cc . -n B -s

dead-code:
	docker compose run --rm --no-deps --build pipeline vulture . --min-confidence 100

security:
	docker compose run --rm --no-deps --build pipeline bandit -q -r . -x ./tests
	docker compose run --rm --no-deps --build pipeline pip-audit --strict

test: test-unit test-integration

test-unit:
	docker compose run --rm --no-deps --build pipeline pytest -q -m unit --cov=pipeline --cov-report=term-missing --cov-report=xml:coverage.xml

test-integration: bootstrap
	docker compose run --rm --build pipeline pytest -q -m integration

status:
	docker compose exec -T postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN ('\''raw'\'', '\''trusted'\'', '\''delivery'\'') ORDER BY 1, 2;"'

down:
	docker compose down

reset:
	docker compose down -v
