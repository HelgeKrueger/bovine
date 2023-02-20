import pytest
import os

from .models import StoredObject, CollectionItem, VisibleTo

from .permissions import has_access
from .store import ObjectStore


@pytest.fixture
async def store():
    db_file = "test_db.db"
    db_url = f"sqlite://{db_file}"
    store = ObjectStore(db_url)

    await store.init_connection()

    yield store
    await store.close_connection()
    os.unlink(db_file)


async def test_has_access_for_owner(store):
    entry = await StoredObject.create(id="first", owner="owner", content={})

    assert await has_access(entry, "owner")
    assert not await has_access(entry, "other")


async def test_has_access_for_other_in_list(store):
    entry = await StoredObject.create(id="first", owner="owner", content={})

    await VisibleTo.create(main_object=entry, object_id="list")
    await CollectionItem.create(part_of="list", object_id="other")

    assert await has_access(entry, "other")
