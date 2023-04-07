# Citation for the following code:
# Date: 04/06/2023
# Copied from /OR/ Adapted from /OR/ Based on:
# https://unix.stackexchange.com/questions/235223/makefile-include-env-file

include .env
export

all: venv

run: 
	poetry run uvicorn what_the_fec.main:create_app --factory

docker-up:
	cd docker && docker-compose up -d

docker-down:
	cd docker && docker-compose down

dev: docker-up
	poetry run uvicorn what_the_fec.main:create_app --factory --reload

fmt:
	poetry run isort .
	poetry run black .

test:
	poetry run pytest .

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: all run fmt test clean docker-up