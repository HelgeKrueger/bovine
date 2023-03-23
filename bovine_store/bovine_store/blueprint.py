import logging
from urllib.parse import urljoin

from quart import Blueprint, g, request, current_app, render_template, redirect

from bovine.activitystreams.utils import is_public

from .utils import determine_summary

logger = logging.getLogger(__name__)

bovine_store_blueprint = Blueprint(
    "bovine_store", __name__, template_folder="../templates/"
)

public_object_cache = {}


@bovine_store_blueprint.get("/<uuid>")
async def retrieve_from_store(uuid):
    logger.info("Request for uuid %s", uuid)

    object_path = urljoin(current_app.config["host"], request.path)

    if g.retriever is None or g.retriever == "NONE":
        if "text" not in request.headers.get("accept"):
            return {"status": "unauthorized"}, 401

        return await fallback_handler(object_path)

    if object_path in public_object_cache:
        logger.info("Serving from cache")
        return (
            public_object_cache[object_path],
            200,
            {"content-type": "application/activity+json"},
        )

    store = current_app.config["bovine_store"]

    obj = await store.retrieve(g.retriever, object_path)

    if is_public(obj):
        public_object_cache[object_path] = obj

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


async def fallback_handler(object_path):
    object_type = None
    object_summary = None
    store = current_app.config["bovine_store"]
    obj = await store.retrieve("Public", object_path)

    if obj:
        if obj.get("url"):
            return redirect(obj.get("url"))
        object_type = obj.get("type")
        object_summary = determine_summary(obj)

    return (
        await render_template(
            "fallback.html",
            object_path=object_path,
            object_type=object_type,
            object_summary=object_summary,
        ),
        415,
    )
