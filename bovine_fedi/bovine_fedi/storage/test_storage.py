from bovine_fedi.utils.test import db_url  # noqa: F401

from .storage import Storage


async def test_storage(db_url):  # noqa F811
    storage = Storage()

    assert await storage.get_object("name") is None

    data = b"\x13\x00\x00\x00\x08\x00"

    assert await storage.add_object("name", data)

    result = await storage.get_object("name")

    assert result.data == data
