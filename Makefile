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
	docker compose run --rm report sh -c "python -m pytest -q"

run-report:
	docker compose run --rm report

docker-build:
	docker compose build

docker-run:
	docker compose run --rm report

report:
	# Execute notebook and export HTML report entirely inside the container
	docker compose run --rm report sh -c "python -m nbconvert --to notebook --execute biodiversity.ipynb --ExecutePreprocessor.timeout=600 --output biodiversity-executed.ipynb && python -m nbconvert --to html biodiversity-executed.ipynb --output report.html"

install-precommit:
	docker compose run --rm report sh -c "pip install pre-commit && pre-commit install --install-hooks"

