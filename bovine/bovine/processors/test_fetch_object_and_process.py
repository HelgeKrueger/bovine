import json
from unittest.mock import AsyncMock, patch

from bovine.types import InboxItem, LocalUser

from .fetch_object_and_process import fetch_object_and_process


@patch("bovine_core.clients.signed_http.signed_get")
async def test_fetch_object_and_process(mock_signed_get):
    mock_process = AsyncMock()
    local_user = LocalUser(
        "name", "url", "public_key", "private_key", "actor_type"
    ).set_inbox_process(mock_process)
    item = InboxItem(json.dumps({"type": "Announce", "object": "url"}))

    result = await fetch_object_and_process(item, local_user, None)

    mock_signed_get.assert_awaited_once()
    mock_process.assert_awaited_once()

    assert result == item
