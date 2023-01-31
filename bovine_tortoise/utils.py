import os

import pytest
from tortoise import Tortoise

from . import init


@pytest.fixture
async def db_url() -> str:
    db_file = "test_db.sqlite3"
    db_url = f"sqlite://{db_file}"

    await init(db_url)

    yield db_url

    await Tortoise.close_connections()

    os.unlink(db_file)
