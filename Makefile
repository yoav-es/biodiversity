PYTHON := python
PIP := $(PYTHON) -m pip

.PHONY: help test run-report docker-build docker-run install-precommit

help:
	@echo "Available targets:"
	@echo "  make test         - run pytest"
	@echo "  make run-report   - execute the notebook and save executed artifact"
	@echo "  make docker-build - build the docker image"
	@echo "  make docker-run   - run the report in docker (writes executed notebook)"
	@echo "  make install-precommit - install pre-commit hooks"

test:
	$(PYTHON) -m pytest -q

run-report:
	bash scripts/run_report.sh

docker-build:
	docker compose build

docker-run:
	docker compose run --rm report

install-precommit:
	$(PIP) install pre-commit
	pre-commit install

