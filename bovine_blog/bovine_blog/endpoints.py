import json
import logging
from urllib.parse import urljoin

from bovine.server.rewrite_request import add_authorization_to_request
from bovine.types import ProcessingItem
from bovine.utils.server import ordered_collection_responder
from bovine_core.types import Visibility
from bovine_store.store.collection import collection_count, collection_items
from bovine_user.types import EndpointType
from quart import Blueprint, current_app, g, request
from quart_auth import current_user

from .process.process import default_outbox_process, process_inbox, send_outbox_item
from .utils import update_id

# from .process.content.store_incoming import add_incoming_to_outbox


async def add_authorization():
    await add_authorization_to_request()

    g.retriever = "NONE"

    if g.signature_result:
        g.retriever = g.signature_result.split("#")[0]
        return

    if current_user.is_authenticated:
        manager = current_app.config["bovine_user_manager"]
        _, actor = await manager.get_activity_pub(current_user.auth_id)
        if actor:
            g.retriever = actor.build()["id"]
            return

        logging.warning("Unknown auth id %s", current_user.auth_id)


logger = logging.getLogger(__name__)

endpoints = Blueprint("endpoint", __name__)
endpoints.before_request(add_authorization)


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

    retriever = g.retriever

    if endpoint_information.endpoint_type == EndpointType.ACTOR:
        activity_pub, actor = await manager.get_activity_pub(
            endpoint_information.bovine_user.hello_sub
        )

        if endpoint_path == retriever:
            return (
                actor.build(visibility=Visibility.OWNER),
                200,
                {"content-type": "application/activity+json"},
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

    actor = actor.build(visibility=Visibility.OWNER)

    if endpoint_type == EndpointType.INBOX:
        if not g.signature_result:
            return {"status": "unauthorized"}, 401

        current_app.add_background_task(process_inbox, request, activity_pub, actor)
        return {"status": "processing"}, 202

    if g.retriever != actor["id"]:
        return {"status": "unauthorized"}, 401

    if endpoint_type == EndpointType.OUTBOX:
        store = current_app.config["bovine_store"]
        data = await request.get_json()

        data = await update_id(data, actor["id"], store)

        new_id = data["id"]

        result = await store.store(actor["id"], data)
        item = ProcessingItem(json.dumps(data))
        await default_outbox_process(item, activity_pub, actor)

        current_app.add_background_task(send_outbox_item, item, activity_pub, actor)

        logger.debug(result)

        return {"status": "created"}, 201, {"location": new_id}

    if endpoint_type == EndpointType.PROXY_URL:
        return await proxy_url_response(activity_pub, actor)


async def proxy_url_response(activity_pub, actor):
    await request.get_data(parse_form_data=True)

    logger.info(await request.form)

    url = (await request.form)["id"]
    object_store = current_app.config["bovine_store"]

    if object_store:
        data = await object_store.retrieve(
            actor["id"], url, include=["object", "actor"]
        )
        if data:
            return data, 200

    response = await activity_pub.get(url)

    # data = json.loads(await response.text())
    logger.info(response)

    await object_store.store("FIXME", response, visible_to=[actor["id"]])

    return response, 200
