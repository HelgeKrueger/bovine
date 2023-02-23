import os

import pytest

from bovine_store.store import ObjectStore


@pytest.fixture
async def store():
    db_file = "test_db.db"
    db_url = f"sqlite://{db_file}"
    store = ObjectStore(db_url)

    await store.init_connection()

    yield store
    await store.close_connection()
    os.unlink(db_file)
