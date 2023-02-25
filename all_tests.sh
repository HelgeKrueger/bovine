#!/usr/bin/env bash

set -eux

cd bovine_core
poetry run pytest
poetry run isort .
poetry run black .
# poetry run flake8 .

cd ../bovine
poetry run pytest
# poetry run isort .
poetry run black .
poetry run flake8 .

cd ../bovine_store
poetry run pytest
# poetry run isort .
poetry run black .
poetry run flake8 .

cd ../bovine_tortoise
poetry run pytest
poetry run isort .
poetry run black .
poetry run flake8 .

cd ../bovine_blog
poetry run pytest
poetry run isort .
poetry run black .
poetry run flake8 .

cd ../tests
poetry run pytest
# poetry run isort .
poetry run black .
poetry run flake8 .

cd ../docs
python make_specification.py
poetry run mdformat .

cd ..

ack '# FIXME' bovine* tests
