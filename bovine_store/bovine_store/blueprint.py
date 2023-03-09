import logging
from urllib.parse import urljoin

from quart import Blueprint, g, request, current_app

logger = logging.getLogger(__name__)

bovine_store_blueprint = Blueprint("bovine_store", __name__)


@bovine_store_blueprint.get("/<uuid>")
async def retrieve_from_store(uuid):
    logger.info("Request for uuid %s", uuid)

    if g.retriever is None or g.retriever == "NONE":
        return {"status": "unauthorized"}, 401

    object_path = urljoin(current_app.config["host"], request.path)

    store = current_app.config["bovine_store"]

    obj = await store.retrieve(g.retriever, object_path)

    if obj:
        return obj, 200, {"content-type": "application/activity+json"}

    return (
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Tombstone",
            "id": object_path,
            "name": "Ceci n'est pas un object",
        },
        404,
        {"content-type": "application/activity+json"},
    )
