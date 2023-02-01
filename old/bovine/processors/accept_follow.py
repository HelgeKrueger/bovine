from quart import current_app

import bovine.clients
from bovine.activitystreams.activities import build_accept
from bovine.types import InboxItem, LocalUser


async def accept_follow_request(
    item: InboxItem,
    local_user: LocalUser,
) -> InboxItem | None:
    data = item.get_data()

    if data["type"] != "Follow":
        return item

    request_data = build_accept(local_user.url, data).build()

    inbox = data["actor"] + "/inbox"

    await bovine.clients.send_activitypub_request(
        current_app.config["session"], inbox, request_data, local_user
    )

    return None
