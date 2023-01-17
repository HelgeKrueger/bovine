import pytest
import os
from tortoise import Tortoise

from bovine.stores import LocalUser
from bovine.processors import InboxItem

from . import init, ManagedDataStore
from .processors import store_in_database


@pytest.fixture
async def db_url():
    db_file = "test_db.sqlite3"
    db_url = f"sqlite://{db_file}"

    await init(db_url)

    yield db_url

    await Tortoise.close_connections()

    os.unlink(db_file)


async def test_basic_data_store(db_url):
    store = ManagedDataStore(db_url=db_url)

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    await store.add_user(local_user)

    result = await store.get_user("other")

    assert result is None

    result = await store.get_user("name")

    assert result.name == "name"


async def test_store_in_database(db_url):
    store = ManagedDataStore(db_url=db_url)

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    await store.add_user(local_user)

    item = InboxItem({}, {})

    await store_in_database(local_user, item)
