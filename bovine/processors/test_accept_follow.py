import json
import pytest
from unittest.mock import patch

from bovine.user_store import LocalUser
from . import InboxItem
from .accept_follow import accept_follow_request


@pytest.mark.asyncio
async def test_returns_item_if_not_a_follow_request():
    item = InboxItem({}, json.dumps({"type": "Avoid"}))
    result = await accept_follow_request(None, item)

    assert item == result


@pytest.mark.asyncio
@patch("bovine.clients.send_activitypub_request")
async def test_on_follow_makes_a_request_to_send_activity(
    mock_send_activitypub_request,
):
    mock_send_activitypub_request.return_value = None

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    item = InboxItem({}, json.dumps({"type": "Follow", "actor": "url"}))
    await accept_follow_request(local_user, item)

    mock_send_activitypub_request.assert_called_once()
