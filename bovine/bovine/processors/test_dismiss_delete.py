import json
from unittest.mock import AsyncMock

from bovine.types import InboxItem

from .dismiss_delete import dismiss_delete


async def test_dismiss_delete_callback_is_called():
    mock = AsyncMock()

    item = InboxItem(json.dumps({"type": "Delete"}))

    coroutine = dismiss_delete(mock)

    await coroutine(item, None, None)

    mock.assert_awaited_once()


async def test_dismiss_delete_callback_is_not_called():
    mock = AsyncMock()

    item = InboxItem(json.dumps({"type": "Follow"}))

    coroutine = dismiss_delete(mock)

    await coroutine(item, None, None)

    mock.assert_not_awaited()
