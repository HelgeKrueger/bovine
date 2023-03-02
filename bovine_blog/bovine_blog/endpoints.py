import json
import logging
from urllib.parse import urljoin

from bovine.server.rewrite_request import add_authorization_to_request
from bovine.types import ProcessingItem
from bovine.utils.server import ordered_collection_responder
from bovine_store.store.collection import collection_count, collection_items
from bovine_user.types import EndpointType
from quart import Blueprint, current_app, g, request

from .process.process import default_outbox_process, process_inbox

# from .process.content.store_incoming import add_incoming_to_outbox

logger = logging.getLogger(__name__)

endpoints = Blueprint("endpoint", __name__)
endpoints.before_request(add_authorization_to_request)


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

    authorized_user = g.signature_result
    if authorized_user is None:
        retriever = "NONE"
    else:
        retriever = authorized_user.split("#")[0]

    logger.info("Retrieving %s for %s", endpoint_path, retriever)

    async def ccount():
        return await collection_count(retriever, endpoint_path)

    async def citems(**kwargs):
        return await collection_items(retriever, endpoint_path, **kwargs)

    return await ordered_collection_responder(
        endpoint_path,
        ccount,
        citems,
        **arguments,
    )


@endpoints.post("/<identifier>")
async def endpoints_post(identifier):
    hostname = current_app.config["host"]
    manager = current_app.config["bovine_user_manager"]

    endpoint_path = urljoin(hostname, request.path)
    endpoint_information = await manager.resolve_endpoint(endpoint_path)
    endpoint_type = endpoint_information.endpoint_type

    if endpoint_type not in [
        EndpointType.INBOX,
        EndpointType.OUTBOX,
        EndpointType.PROXY_URL,
    ]:
        return {"status": "method not allowed"}, 405

    activity_pub, actor = await manager.get_activity_pub(
        endpoint_information.bovine_user.hello_sub
    )

    actor = actor.build()

    if endpoint_type == EndpointType.INBOX:
        current_app.add_background_task(process_inbox, request, activity_pub, actor)

    if endpoint_type == EndpointType.OUTBOX:
        store = current_app.config["bovine_store"]
        data = await request.get_json()

        data["id"] = await store.id_generator()
        if "object" in data:
            data["object"]["id"] = await store.id_generator()

        result = await store.store(actor["id"], data)
        item = ProcessingItem(json.dumps(data))
        await default_outbox_process(item, activity_pub, actor)

        logger.info(result)

        return {"status": "created"}, 201
        # current_app.add_background_task(process_outbox, request, activity_pub, actor)

    if endpoint_type == EndpointType.PROXY_URL:
        return await proxy_url_response(activity_pub, actor)

    return {"status": "processing"}, 202


async def proxy_url_response(activity_pub, actor):
    await request.get_data(parse_form_data=True)

    logger.info(await request.form)

    url = (await request.form)["id"]
    object_store = current_app.config["object_store"]

    if object_store:
        data = await object_store.retrieve(actor["id"], url, include=["object"])
        if data:
            return data, 200

    response = await activity_pub.get(url)

    data = json.loads(await response.text())

    if object_store:
        await object_store.store("FIXME", data, visible_to=[actor["id"]])

    return data, 200
