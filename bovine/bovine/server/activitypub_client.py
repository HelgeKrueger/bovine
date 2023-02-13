import asyncio
import json
import logging

import werkzeug
from bovine_core.clients.signed_http import signed_get
from quart import Blueprint, current_app, g, request, abort, make_response
from quart_cors import route_cors

from bovine.types import ProcessingItem
from bovine.utils.server import ordered_collection_responder


from .activitypub import cors_properties

activitypub_client = Blueprint(
    "activitypub_client", __name__, url_prefix="/activitypub"
)

logger = logging.getLogger(__name__)


def has_authorization(local_user) -> bool:
    authorized_user = g.get("authorized_user")
    used_public_key = g.get("signature_result")

    if local_user is None:
        account_name = None
        public_key_url = None
    else:
        account_name = local_user.name
        public_key_url = local_user.get_public_key_url()

    if authorized_user is None:
        if used_public_key is None:
            logger.warning(
                "Request for "
                + str(account_name)
                + " at "
                + str(request.path)
                + " with "
                + str(request.method)
                + " without authorization",
            )
            return False

        logging.info(public_key_url)
        logging.info(used_public_key)

        if public_key_url != used_public_key:
            logger.warning(
                "Request for "
                + str(account_name)
                + " at "
                + str(request.path)
                + " with "
                + str(request.method)
                + " with authorization for wrong user",
            )
            return False

    elif authorized_user != account_name:
        logger.warning(
            "Request for "
            + str(account_name)
            + " at "
            + str(request.path)
            + " with "
            + str(request.method)
            + " with authorization for wrong user",
        )
        return False

    return True


@activitypub_client.get("/<account_name>/inbox")
@route_cors(**cors_properties)
async def inbox_get(account_name: str):
    local_actor = await current_app.config["get_user"](account_name)

    if not has_authorization(local_actor):
        return {"status": "access denied"}, 401

    return await ordered_collection_responder(
        local_actor.get_inbox(),
        local_actor.item_count_for("inbox"),
        local_actor.items_for("inbox"),
        **{
            name: request.args.get(name)
            for name in ["first", "last", "min_id", "max_id"]
            if request.args.get(name) is not None
        },
    )


@activitypub_client.post("/<account_name>/outbox")
@route_cors(**cors_properties)
async def post_outbox(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    content_type = request.headers.get("content-type")
    if content_type and content_type.startswith("multipart"):
        await request.get_data(parse_form_data=True)
    else:
        await request.get_data()

    local_user = await current_app.config["get_user"](account_name)
    if not has_authorization(local_user):
        return {"status": "access denied"}, 401

    if request.headers["content-type"].startswith("multipart"):
        files = await request.files
        form = await request.form
        for key in files.keys():
            await current_app.config["object_storage"].add_object(
                key, files[key].read()
            )
        activity = json.loads(form["activity"])
    else:
        activity = await request.get_json()

    await local_user.process_outbox_item(activity, current_app.config["session"])

    return {"status": "success"}, 202


@activitypub_client.post("/<account_name>/fetch")
@route_cors(**cors_properties)
async def fetch(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    raw_data = await request.get_data()

    local_user = await current_app.config["get_user"](account_name)
    if not has_authorization(local_user):
        return {"status": "access denied"}, 401

    data = json.loads(raw_data)

    logger.info(f"Fetching {data['url']} for {account_name}")

    response = await signed_get(
        current_app.config["session"],
        local_user.get_public_key_url(),
        local_user.private_key,
        data["url"],
    )

    inbox_item = ProcessingItem(await response.text())

    await local_user.process_inbox_item(inbox_item, current_app.config["session"])

    return {"status": "success"}, 200


@activitypub_client.get("/<actor_name>/serverSideEvents")
@route_cors(**cors_properties)
async def sse(actor_name: str):
    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)

    queue_manager = current_app.config["queue_manager"]

    local_user = await current_app.config["get_user"](actor_name)
    if not has_authorization(local_user):
        return {"status": "access denied"}, 401

    logger.info(f"Opening stream for {actor_name}")

    queue_id, queue = queue_manager.new_queue_for_actor(actor_name)

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
                queue_manager.remove_queue_for_actor(actor_name, queue_id)

                logger.info(f"Removing {queue_id} from {actor_name}")
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
    return response


@activitypub_client.post("/<account_name>/proxyUrl")
@route_cors(allow_origin=["http://localhost:8000"], allow_methods=["POST"])
async def proxy_url(account_name: str) -> tuple[dict, int]:
    await request.get_data(parse_form_data=True)

    local_user = await current_app.config["get_user"](account_name)
    if not has_authorization(local_user):
        return {"status": "access denied"}, 401

    url = (await request.form)["id"]

    logger.info(f"Fetching {url} for {account_name}")

    response = await signed_get(
        current_app.config["session"],
        local_user.get_public_key_url(),
        local_user.private_key,
        url,
    )

    data = json.loads(await response.text())

    return data, 200
