setup:
	asdf install
	poetry install --extras sqlalchemy

fmt:
	poetry run black .
	poetry run isort .

clean:
	rm -rf dist

build:
	poetry build

publish: clean build
	poetry publish

release: clean build
	ghr -u crflynn -r databricks-dbapi -c $(shell git rev-parse HEAD) -delete -b "release" -n $(shell poetry version | tail -c +18) $(shell poetry version | tail -c +18) dist
