import asyncio
import json
import logging
import re
from urllib.parse import urljoin

from bovine.types import Visibility
from bovine.utils.crypto import content_digest_sha256
from bovine_process.process import (
    default_outbox_process,
    process_inbox,
    send_outbox_item,
)
from bovine_process.types.processing_item import ProcessingItem
from bovine_store.collection import collection_response
from bovine_user.types import EndpointType
from quart import Blueprint, current_app, g, make_response, request
from quart_auth import current_user

from .utils import update_id

# from .process.content.store_incoming import add_incoming_to_outbox


def is_get():
    return re.match(r"^get$", request.method, re.IGNORECASE)


def is_post():
    return re.match(r"^post$", request.method, re.IGNORECASE)


async def compute_signature_result() -> str | None:
    if is_get():
        return await current_app.config["validate_signature"](request, digest=None)

    if is_post():
        raw_data = await request.get_data()
        digest = content_digest_sha256(raw_data)
        return await current_app.config["validate_signature"](request, digest=digest)

    return None


async def add_authorization():
    g.signature_result = await compute_signature_result()

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

    if endpoint_information.endpoint_type == EndpointType.ACTOR:
        activity_pub, actor = await manager.get_activity_pub(
            endpoint_information.bovine_user.hello_sub
        )

        if endpoint_path == g.retriever:
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

    if endpoint_information.endpoint_type == EndpointType.EVENT_SOURCE:
        activity_pub, actor = await manager.get_activity_pub(
            endpoint_information.bovine_user.hello_sub
        )
        actor = actor.build(visibility=Visibility.OWNER)
        if g.retriever != actor["id"]:
            return {"status": "unauthorized"}, 401
        return await handle_event_source(endpoint_path, activity_pub, actor)

    return await collection_response(endpoint_path)


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

    await object_store.store("FIXME", response, visible_to=[actor["id"]])

    return response, 200


async def handle_event_source(endpoint_path, activity_pub, actor):
    if endpoint_path != actor["endpoints"]["eventSource"]:
        return {"status": "unauthorized"}, 401

    logger.info("Opening event source for %s", actor["name"])

    queue_manager = current_app.config["queue_manager"]
    queue_id, queue = queue_manager.new_queue_for_actor(endpoint_path)

    async def send_events():
        while True:
            try:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=10)
                    logger.debug(f"Sending event {event.encode()}")
                    yield event.encode()
                    queue.task_done()
                except asyncio.TimeoutError:
                    yield (":" + " " * 2048 + "\n").encode("utf-8")

            except asyncio.CancelledError as e:
                queue_manager.remove_queue_for_actor(endpoint_path, queue_id)

                logger.info("Removing %s from %s", queue_id, actor["name"])
                raise e

    response = await make_response(
        send_events(),
        {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
        },
    )
    response.timeout = None

    # last_event_id = request.headers.get("last-event-id")
    # if last_event_id:
    #     current_app.add_background_task(
    #         enqueue_missing_events, queue, last_event_id, actor["name"]
    #     )

    return response
