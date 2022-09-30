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

version:
	@git add pyproject.toml
	@git commit -m "$$(poetry version -s)"
	@git tag --sign "v$$(poetry version -s)" -m "$(poetry version -s)"
	@git push --follow-tags

.PHONY: build format lint server smoketest test watch version
