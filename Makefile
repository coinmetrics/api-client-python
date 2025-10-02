.PHONY:  all fetch-openapi-spec build-schema check clean docs image imagetest test venv

# default image name
IMAGE = api-client-image
# default virtual environment name
VENV = .venv-api

all: build-schema check test

fetch-openapi-spec:
	curl -o openapi.yaml https://docs.coinmetrics.io/api/static/openapi.yaml

build-schema:
	python coinmetrics/build.py

venv:
	rm -rf ./$(VENV)
	python3.11 -m venv ./$(VENV)
	./$(VENV)/bin/pip install -U pip setuptools
	./$(VENV)/bin/pip install poetry
	. ./$(VENV)/bin/activate && poetry install --with dev
	@echo "To use virtual environment run 'source ./$(VENV)/bin/activate'"

check:
	python -m mypy -p coinmetrics -p test
	python -m flake8 coinmetrics

# NOTE: requires CM_API_KEY with employee permissioning
test:
	TZ=UTC python -m pytest -n auto --timeout=60 test --ignore test/test_data_exporter.py --ignore test/test_rate_limits.py  --ignore test/test_catalog.py --ignore test/test_catalog_benchmarks.py
	python -m pytest test/test_rate_limits.py

# Run all tests including those normally skipped by the CI/CD pipeline
all-tests: test
	python -m pytest test/test_data_exporter.py test/test_catalog.py test/test_catalog_benchmarks.py

docs:
	pydoc-markdown -m coinmetrics.api_client > docs/docs/reference/api_client.md
	cp -f README.md docs/docs/index.md
	cp -f CHANGELOG.md docs/docs/releases/CHANGELOG.md
	cp -f examples/README.md docs/docs/user-guide/examples.md
	cd docs && mkdocs build

image:
	docker build --tag $(IMAGE) .

imagetest:
	docker run --rm $(IMAGE) python -m mypy -p coinmetrics -p test
	docker run --rm $(IMAGE) python -m flake8 coinmetrics
	docker run -e CM_API_KEY=$(CM_API_KEY) --rm $(IMAGE) python -m pytest -n auto --timeout=60 test --ignore test/test_data_exporter.py --ignore test/test_rate_limits.py  --ignore test/test_catalog.py --ignore test/test_catalog_benchmarks.py
	docker run -e CM_API_KEY=$(CM_API_KEY) --rm $(IMAGE) python -m pytest test/test_rate_limits.py

clean:
	rm -rf ./cm_api_client_debug_*.txt
	rm -f coinmetrics/_schema_constants.py
