import json
from unittest.mock import patch

from bovine.types import LocalUser, InboxItem

from .test_database import db_url  # noqa: F401
from .models import Actor, Follower

from .processors import accept_follow_request


@patch("bovine.clients.send_activitypub_request")
async def test_accept_follow_request(
    mock_send_activitypub_request,
    db_url,  # noqa: F811
):
    actor = await Actor.create(
        account="name",
        url="url",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )

    local_user = LocalUser("name", "url", "public_key", "private_key", "actor_type")

    item = InboxItem({}, json.dumps({"type": "Follow", "actor": "url"}))
    result = await accept_follow_request(local_user, item)

    assert result is None

    mock_send_activitypub_request.assert_called_once()

    followers = Follower.filter(actor=actor)
    assert await followers.count() == 1

    follower = await followers.get()

    assert follower.account == "url"
