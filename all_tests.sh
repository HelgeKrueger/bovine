#!/usr/bin/env bash

set -eux

cd bovine
#poetry lock
#poetry install
poetry run pytest
poetry run isort .
poetry run black .
# poetry run flake8 .

cd ../bovine_store
#poetry lock
#poetry install
poetry run pytest
# poetry run isort .
poetry run black .
poetry run flake8 .

cd ../bovine_user
#poetry lock
#poetry install
poetry run pytest
poetry run isort .
poetry run black .
poetry run flake8 .

cd ../bovine_process
#poetry lock
#poetry install
poetry run pytest
poetry run isort .
poetry run black .
poetry run flake8 .

cd ../bovine_fedi
#poetry lock
#poetry install
poetry run pytest
poetry run isort .
poetry run black .
#poetry run flake8 .

cd ../tests
#poetry lock
#poetry install
poetry run pytest
# poetry run isort .
poetry run black .
poetry run flake8 .

cd ../docs
python make_specification.py
poetry run mdformat .

cd ..

ack '# FIXME' bovine* tests
