
all: venv

run: 
	poetry run uvicorn what_the_fec.main:create_app --factory

dev: 
	poetry run uvicorn what_the_fec.main:create_app --factory --reload

fmt:
	poetry run isort .
	poetry run black .

test:
	poetry run pytest .

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: all run fmt test clean