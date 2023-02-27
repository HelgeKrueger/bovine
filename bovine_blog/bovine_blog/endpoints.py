from urllib.parse import urljoin

from bovine.utils.server import ordered_collection_responder
from bovine_store.store.collection import collection_count, collection_items
from bovine_user.types import EndpointType
from quart import Blueprint, current_app, request

endpoints = Blueprint("endpoint", __name__)


@endpoints.get("/<identifier>")
async def endpoints_get(identifier):
    hostname = current_app.config["host"]

    endpoint_path = urljoin(hostname, request.path)

    manager = current_app.config["bovine_user_manager"]

    endpoint_information = await manager.resolve_endpoint(endpoint_path)

    if endpoint_information is None:
        return (
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Object",
                "id": endpoint_path,
                "name": "Ceci n'est pas un object",
            },
            404,
            {"content-type": "application/activity+json"},
        )

    if endpoint_information.endpoint_type == EndpointType.ACTOR:
        activity_pub, actor = await manager.get_activity_pub(
            endpoint_information.bovine_user.hello_sub
        )

        return (
            actor.build(),
            200,
            {"content-type": "application/activity+json"},
        )

    arguments = {
        name: request.args.get(name)
        for name in ["first", "last", "min_id", "max_id"]
        if request.args.get(name) is not None
    }

    async def ccount():
        return await collection_count("retriever", endpoint_path)

    async def citems(**kwargs):
        return await collection_items("retriever", endpoint_path, **kwargs)

    return await ordered_collection_responder(
        endpoint_path,
        ccount,
        citems,
        **arguments,
    )
