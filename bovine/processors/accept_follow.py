import bovine.clients
from bovine.activitystreams.activities import build_accept
from bovine.user_store import LocalUser
from . import InboxItem


async def accept_follow_request(
    local_user: LocalUser, item: InboxItem
) -> InboxItem | None:
    data = item.get_data()

    if data["type"] != "Follow":
        return item

    request_data = build_accept(local_user.url, data).build()

    inbox = data["actor"] + "/inbox"

    await bovine.clients.send_activitypub_request(inbox, request_data, local_user)
