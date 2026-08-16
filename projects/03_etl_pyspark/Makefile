.DEFAULT_GOAL := run

.PHONY: up run format-check docformat-check lint type-check complexity dead-code architecture security test test-unit test-integration status down reset

up:
	docker compose up -d --wait postgres

run: up
	docker compose run --rm --build spark

format-check:
	docker compose run --rm --no-deps --build spark ruff format --check .

docformat-check:
	docker compose run --rm --no-deps --build spark pydocstringformatter --exit-code --quiet .

lint:
	docker compose run --rm --no-deps --build spark ruff check .

type-check:
	docker compose run --rm --no-deps --build spark mypy .

complexity:
	docker compose run --rm --no-deps --build spark radon cc . -n B -s

dead-code:
	docker compose run --rm --no-deps --build spark vulture . --min-confidence 100

architecture:
	docker compose run --rm --no-deps --build spark lint-imports --config /app/.importlinter

security:
	docker compose run --rm --no-deps --build spark bandit -q -r . -x ./tests
	docker compose run --rm --no-deps --build spark pip-audit --strict

test: test-unit test-integration

test-unit:
	docker compose run --rm --no-deps --build spark pytest -q -m unit --cov=pipeline --cov-fail-under=95 --cov-report=term-missing --cov-report=xml:coverage.xml --junitxml=junit-unit.xml

test-integration: up
	docker compose run --rm --build spark pytest -q -m integration --junitxml=junit-integration.xml

status:
	docker compose exec -T postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "SELECT count(*) AS registros FROM reclamacoes_consolidadas;"'

down:
	docker compose down

reset:
	docker compose down -v
