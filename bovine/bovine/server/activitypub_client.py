import json
import logging

import werkzeug
from bovine_core.clients.signed_http import signed_get
from quart import Blueprint, current_app, g, request
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
@route_cors(allow_origin=["http://localhost:8000"], allow_methods=["POST"])
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
