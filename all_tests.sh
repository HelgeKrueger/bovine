#!/usr/bin/env bash

set -eux

cd bovine_core
poetry run pytest
poetry run isort .
poetry run black .
# poetry run flake8 .

cd ../bovine_store
poetry run pytest
# poetry run isort .
poetry run black .
poetry run flake8 .

cd ../bovine_user
poetry run pytest
poetry run isort .
poetry run black .
poetry run flake8 .

cd ../bovine_process
poetry run pytest
poetry run isort .
poetry run black .
poetry run flake8 .

cd ../bovine_fedi
poetry run pytest
poetry run isort .
poetry run black .
#poetry run flake8 .

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
