from unittest.mock import AsyncMock

from bovine_tortoise.models import PublicKey
from bovine_tortoise.utils.test import db_url  # noqa: F401

from .public_key import PublicKeyCache


async def test_public_key(db_url):  # noqa F811
    key_fetcher = AsyncMock()
    key_fetcher.return_value = "---key---"
    url = "proto://domain/path#id"

    public_key_cache = PublicKeyCache(key_fetcher)
    public_key = await public_key_cache.get_for_url(url)

    assert public_key == "---key---"

    key_fetcher.assert_awaited_once()

    item = await PublicKey.get(url=url)

    assert item.public_key == "---key---"


async def test_public_key_handles_return_null(db_url):  # noqa F811
    key_fetcher = AsyncMock()
    key_fetcher.return_value = None
    url = "proto://domain/path#id"

    public_key_cache = PublicKeyCache(key_fetcher)
    public_key = await public_key_cache.get_for_url(url)

    assert public_key is None
    key_fetcher.assert_awaited_once()

    assert await PublicKey.filter().count() == 0


async def test_public_key_only_fetches_once(db_url):  # noqa F811
    key_fetcher = AsyncMock()
    key_fetcher.return_value = "---key---"
    url = "proto://domain/path#id"

    public_key_cache = PublicKeyCache(key_fetcher)
    public_key = await public_key_cache.get_for_url(url)
    assert public_key == "---key---"

    public_key = await public_key_cache.get_for_url(url)
    assert public_key == "---key---"

    key_fetcher.assert_awaited_once()
