all: lint test

build:
	@rm -rf dist
	@poetry build

clean:
	@rm -rf .pytest-incremental

lint:
	@poetry run pylint ./makenew_python_app

server:
	@poetry run python -m makenew_python_app

smoketest:
	@curl http://localhost:9001/health

publish:
	@poetry run twine upload dist/*

test:
	@poetry run pytest --inc --cov=./makenew_python_app

watch:
	@poetry run ptw

.PHONY: build docs test
