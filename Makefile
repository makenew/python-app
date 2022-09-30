all: build

build:
	@rm -rf dist
	@poetry build

format:
	@poetry run black .

lint:
	@poetry run pylint ./makenew_python_app
	@poetry run black --check .

server:
	@poetry run python -m makenew_python_app

smoketest:
	@curl http://localhost:9001/health

test:
	@poetry run pytest --cov=./makenew_python_app

watch:
	@poetry run ptw

.PHONY: build format lint server smoketest test watch
