.DEFAULT_GOAL := run

.PHONY: up debug parse compile seed build format-check lint test run status down reset

up:
	docker compose up -d --wait postgres

debug: up
	docker compose run --rm --no-deps --build dbt dbt debug

parse: up
	docker compose run --rm --no-deps --build dbt dbt parse

compile: up
	docker compose run --rm --no-deps --build dbt dbt compile

seed: up
	docker compose run --rm --no-deps --build dbt dbt seed --full-refresh

build: up
	docker compose run --rm --no-deps --build dbt dbt build

format-check: lint

lint: up
	docker compose run --rm --no-deps --build dbt sqlfluff lint models

test: run
	docker compose run --rm --no-deps --build dbt dbt test

run: seed build

status: up
	docker compose exec -T postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "SELECT count(*) AS registros FROM public_delivery.mod_final;"'

down:
	docker compose down

reset:
	docker compose down -v
