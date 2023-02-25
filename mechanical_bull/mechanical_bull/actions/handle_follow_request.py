import logging
import json

from bovine_core.activitystreams.activities import build_accept
from bovine_core.activitypub.actor import ActivityPubActor

logger = logging.getLogger(__name__)


async def handle_follow_request(actor: ActivityPubActor, data: dict):
    if data["type"] != "Follow":
        return

    logger.info("Accepting follow request")

    accept = build_accept(actor.actor_id, data).build()

    await actor.send_to_outbox(accept)
