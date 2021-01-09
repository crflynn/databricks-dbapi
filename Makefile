setup:
	asdf install
	poetry install --extras sqlalchemy

fmt:
	poetry run black .
	poetry run isort .