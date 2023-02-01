from unittest.mock import AsyncMock

from .processor_list import ProcessorList


async def test_processor_list():
    processor_list = ProcessorList()

    mock1 = AsyncMock()
    mock2 = AsyncMock()
    mock1.return_value = None

    processor_list.add(mock1).add(mock2)

    item = "item"

    result = await processor_list.apply(item)

    mock1.assert_awaited_once()
    mock2.assert_not_awaited()

    assert result is None
