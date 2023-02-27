import os

import pytest
from tortoise import Tortoise


@pytest.fixture
async def db_url() -> str:
    db_file = "test_db.sqlite3"
    db_url = f"sqlite://{db_file}"

    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["bovine_user.models"]},
    )
    await Tortoise.generate_schemas()

    yield db_url

    await Tortoise.close_connections()

    os.unlink(db_file)
