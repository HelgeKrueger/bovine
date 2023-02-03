from bovine.types import InboxItem, LocalUser

from . import ManagedDataStore
from .processors.inbox import store_in_database
from .utils import db_url  # noqa: F401


async def test_basic_data_store(db_url):  # noqa: F811
    store = ManagedDataStore(db_url=db_url)

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    await store.add_user(local_user)

    result = await store.get_user("other")

    assert result is None

    result = await store.get_user("name")

    assert result.name == "name"


async def test_store_in_database(db_url):  # noqa: F811
    store = ManagedDataStore(db_url=db_url)

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    await store.add_user(local_user)

    item = InboxItem("{}")

    await store_in_database(item, local_user, None)