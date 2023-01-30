import json
from unittest.mock import patch

from bovine.types import InboxItem, LocalUser
from bovine.utils.test.in_memory_test_app import app

from .accept_follow import accept_follow_request


async def test_returns_item_if_not_a_follow_request():
    item = InboxItem(json.dumps({"type": "Avoid"}))
    result = await accept_follow_request(item, None)

    assert item == result


@patch("bovine.clients.send_activitypub_request")
async def test_on_follow_makes_a_request_to_send_activity(
    mock_send_activitypub_request,
):
    async with app.app_context():
        mock_send_activitypub_request.return_value = None

        local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

        item = InboxItem(json.dumps({"type": "Follow", "actor": "url"}))
        await accept_follow_request(item, local_user)

        mock_send_activitypub_request.assert_called_once()
