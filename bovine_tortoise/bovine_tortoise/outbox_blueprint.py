import logging
from urllib.parse import urlparse

from bovine.server.activitypub import has_authorization
from bovine.server.rewrite_request import rewrite_activity_request
from quart import Blueprint, request

from .models import Actor, OutboxEntry

outbox_blueprint = Blueprint("outbox", __name__)
outbox_blueprint.before_request(rewrite_activity_request)

logger = logging.getLogger(__name__)


@outbox_blueprint.get("/<username>/<uuid>")
async def element(username: str, uuid: str):
    request_path = urlparse(request.url).path

    if not has_authorization():
        logger.warning(
            f"Invalid signature on get http request for outbox object {request_path}"
        )
        return {"status": "request not signed"}, 401

    actor = await Actor.get_or_none(account=username)

    if actor is None:
        logger.debug(f"Actor not found for {username}, {uuid}")
        return {"status": "not found"}, 404

    entry = await OutboxEntry.get_or_none(actor=actor, local_path=request_path)

    if entry is None:
        entry = await OutboxEntry.get_or_none(
            actor=actor, local_path=request_path + "/activity"
        )

    if entry is None:
        logger.debug(f"Entry not found for {username}, {uuid}, {request_path}")
        return {"status": "not found"}, 404

    content = entry.content

    if not request_path.endswith("activity") and content["type"] in [
        "Create",
        "Update",
    ]:
        content["object"]["@context"] = content["@context"]
        content = content["object"]

    return content, 200, {"content-type": "application/activity+json"}
