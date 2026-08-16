.DEFAULT_GOAL := quality-ci

.PHONY: gitleaks actionlint hadolint quality-ci

gitleaks:
	docker run --rm -v "$(CURDIR):/repo:ro" zricethezav/gitleaks:v8.18.4 detect --config=/repo/.gitleaks.toml --source=/repo --no-git --redact

actionlint:
	docker run --rm -v "$(CURDIR):/repo:ro" rhysd/actionlint:1.7.7 /repo/.github/workflows/ci-dbt.yml /repo/.github/workflows/ci-pyspark.yml /repo/.github/workflows/ci-python.yml /repo/.github/workflows/ci-governance.yml

hadolint:
	docker run --rm -v "$(CURDIR):/repo:ro" hadolint/hadolint:v2.12.0-debian hadolint --config /repo/.hadolint.yaml /repo/projects/02_etl_python/Dockerfile /repo/projects/03_etl_pyspark/Dockerfile

quality-ci: gitleaks actionlint hadolint
