.DEFAULT_GOAL := run

.PHONY: up bootstrap run status reset down

up:
	docker compose up -d --wait postgres minio

bootstrap: up
	docker compose run --rm --no-deps minio-init

run: bootstrap
	docker compose run --rm --no-deps --build pipeline

status:
	docker compose exec -T postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN ('\''raw'\'', '\''trusted'\'', '\''delivery'\'') ORDER BY 1, 2;"'

down:
	docker compose down

reset:
	docker compose down -v
