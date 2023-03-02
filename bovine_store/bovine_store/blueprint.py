import logging
from urllib.parse import urljoin

from quart import Blueprint, g, request, current_app
from bovine.server.rewrite_request import add_authorization_to_request

logger = logging.getLogger(__name__)

bovine_store_blueprint = Blueprint("bovine_store", __name__)
bovine_store_blueprint.before_request(add_authorization_to_request)


@bovine_store_blueprint.get("/<uuid>")
async def retrieve_from_store(uuid):
    logger.info("Request for uuid %s", uuid)
    # actor_id = g.get("actor_id")

    retriever = None
    try:
        authorized_user = g.signature_result
        retriever = authorized_user.split("#")[0]
    except Exception:
        pass

    if retriever is None:
        return {"status": "unauthorized"}, 401

    object_path = urljoin(current_app.config["host"], request.path)

    store = current_app.config["bovine_store"]

    obj = await store.retrieve(retriever, object_path)

    if obj:
        return obj, 200, {"content-type": "application/activity+json"}

    return (
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Object",
            "id": object_path,
            "name": "Ceci n'est pas un object",
        },
        404,
        {"content-type": "application/activity+json"},
    )
