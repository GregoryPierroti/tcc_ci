.DEFAULT_GOAL := run

.PHONY: up run format-check lint security test status down reset

up:
	docker compose up -d --wait postgres

run: up
	docker compose run --rm --build spark

format-check:
	docker compose run --rm --no-deps --build spark ruff format --check .

lint:
	docker compose run --rm --no-deps --build spark ruff check .

security:
	docker compose run --rm --no-deps --build spark pip-audit --strict

test:
	docker compose run --rm --no-deps --build spark pytest -q --cov=pipeline --cov-report=term-missing --cov-report=xml:coverage.xml

status:
	docker compose exec -T postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "SELECT count(*) AS registros FROM reclamacoes_consolidadas;"'

down:
	docker compose down

reset:
	docker compose down -v
