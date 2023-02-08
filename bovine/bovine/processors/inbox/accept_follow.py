from bovine_core.activitystreams.activities import build_accept
from quart import current_app

import bovine.clients
from bovine.types import ProcessingItem, LocalActor


async def accept_follow_request(
    item: ProcessingItem,
    local_actor: LocalActor,
) -> ProcessingItem | None:
    data = item.get_data()

    if data["type"] != "Follow":
        return item

    request_data = build_accept(local_actor.url, data).build()

    inbox = data["actor"] + "/inbox"

    await bovine.clients.send_activitypub_request(
        current_app.config["session"], inbox, request_data, local_actor
    )

    return None
