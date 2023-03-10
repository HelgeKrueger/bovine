import json
from unittest.mock import AsyncMock, MagicMock

import aiohttp

from bovine.activitystreams import (
    build_ordered_collection,
    build_ordered_collection_page,
)
from bovine.utils.test import get_user_keys

from .activity_pub import ActivityPubClient


async def test_activity_pub_client_get():
    session = AsyncMock(aiohttp.ClientSession)
    url = "https://test_domain/test_path"
    public_key_url = "public_key_url"
    public_key, private_key = get_user_keys()
    session = AsyncMock(aiohttp.ClientSession)
    session.get = AsyncMock()

    client = ActivityPubClient(session, public_key_url, private_key)

    await client.get(url)

    session.get.assert_awaited_once()


async def test_activity_pub_client_get_collection_no_pages():
    session = AsyncMock(aiohttp.ClientSession)
    url = "https://test_domain/test_path"
    public_key_url = "public_key_url"
    public_key, private_key = get_user_keys()
    session = AsyncMock(aiohttp.ClientSession)
    session.get = AsyncMock()

    client = ActivityPubClient(session, public_key_url, private_key)

    text_mock = AsyncMock()
    session.get.return_value = MagicMock(aiohttp.ClientResponse)
    session.get.return_value.text = text_mock

    items = [{"id": j} for j in range(7)]

    builder = build_ordered_collection("url").with_count(7).with_items(items)

    text_mock.return_value = json.dumps(builder.build())

    result = await client.get_ordered_collection(url)
    session.get.assert_awaited_once()

    assert result["total_items"] == 7
    assert result["items"] == items


async def test_activity_pub_client_get_collection_pages():
    session = AsyncMock(aiohttp.ClientSession)
    url = "https://test_domain/test_path"
    public_key_url = "public_key_url"
    public_key, private_key = get_user_keys()
    session = AsyncMock(aiohttp.ClientSession)
    session.get = AsyncMock()

    client = ActivityPubClient(session, public_key_url, private_key)

    text_mock = AsyncMock()
    session.get.return_value = MagicMock(aiohttp.ClientResponse)
    session.get.return_value.text = text_mock

    items = [{"id": j} for j in range(23)]

    builder = (
        build_ordered_collection("url")
        .with_count(23)
        .with_first_and_last("first", "last")
    )

    page_1 = (
        build_ordered_collection_page("url_1", "page_1")
        .with_items(items[:13])
        .with_next("next_1")
    )
    page_2 = (
        build_ordered_collection_page("url_1", "page_2")
        .with_items(items[13:20])
        .with_next("next_2")
    )
    page_3 = build_ordered_collection_page("url_1", "page_2").with_items(items[20:])

    text_mock.side_effect = [
        json.dumps(builder.build()),
        json.dumps(page_1.build()),
        json.dumps(page_2.build()),
        json.dumps(page_3.build()),
    ]

    result = await client.get_ordered_collection(url)

    assert result["total_items"] == 23
    assert result["items"] == items

    text_mock.side_effect = [
        json.dumps(builder.build()),
        json.dumps(page_1.build()),
        json.dumps(page_2.build()),
        json.dumps(page_3.build()),
    ]

    result = await client.get_ordered_collection(url, max_items=17)

    assert result["total_items"] == 23
    assert result["items"] == items[:20]
