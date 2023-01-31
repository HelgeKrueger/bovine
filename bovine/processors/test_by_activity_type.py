from unittest.mock import AsyncMock

from . import build_do_for_types
from .by_activity_type import ByActivityType, do_nothing


async def test_do_nothing():
    item = "item"

    assert await do_nothing(item, "other arg") == item
    assert await do_nothing(item, "other arg", {"more": "arguments"}) == item


async def test_by_activity_type():
    item = {"type": "Test"}

    mock = AsyncMock()
    mock.return_value = "mock"

    by_activity_type = ByActivityType({"Test": mock})

    result = await by_activity_type.act(item)

    assert result == "mock"
    mock.assert_awaited_once()


async def test_build_do_for_types():
    follow_item = {"type": "Follow"}
    create_item = {"type": "Create"}

    mock = AsyncMock()
    mock.return_value = "mock"

    processor = build_do_for_types({"Follow": mock})

    assert await processor(follow_item) == "mock"
    assert await processor(create_item) == create_item

    mock.assert_awaited_once()
