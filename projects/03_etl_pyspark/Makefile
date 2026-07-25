.DEFAULT_GOAL := run

.PHONY: up run test status down reset

up:
	docker compose up -d --wait postgres

run: up
	docker compose run --rm --no-deps --build spark

test:
	docker compose run --rm --no-deps --build spark sh -c 'PYTHONPATH=/app/src pytest -q tests'

status:
	docker compose exec -T postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "SELECT count(*) AS registros FROM reclamacoes_consolidadas;"'

down:
	docker compose down

reset:
	docker compose down -v
