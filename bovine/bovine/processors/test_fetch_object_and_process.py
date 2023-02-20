import json
from unittest.mock import AsyncMock, patch

from bovine.types import ProcessingItem, LocalActor

from bovine.utils.test.in_memory_test_app import app


from .fetch_object_and_process import fetch_object_and_process


@patch("bovine_core.clients.signed_http.signed_get")
async def test_fetch_object_and_process(mock_signed_get):
    mock_process = AsyncMock()
    response = AsyncMock()
    mock_signed_get.return_value = response
    response.text.return_value = "{}"

    local_actor = LocalActor(
        "name", "url", "public_key", "private_key", "actor_type"
    ).set_inbox_process(mock_process)
    item = ProcessingItem(json.dumps({"type": "Announce", "object": "url"}))

    async with app.app_context():
        result = await fetch_object_and_process(item, local_actor)

    mock_signed_get.assert_awaited_once()
    mock_process.assert_awaited_once()

    assert result == item
