import os

import pytest
from tortoise import Tortoise

from bovine_fedi.utils import get_public_private_key_from_files, init


def remove_domain_from_url(url):
    assert url.startswith("https://my_domain")

    return url[17:]


def get_user_keys():
    return get_public_private_key_from_files(
        ".files/public_key.pem", ".files/private_key.pem"
    )


@pytest.fixture
async def db_url() -> str:
    db_file = "test_db.sqlite3"
    db_url = f"sqlite://{db_file}"

    await init(db_url)

    yield db_url

    await Tortoise.close_connections()

    os.unlink(db_file)
