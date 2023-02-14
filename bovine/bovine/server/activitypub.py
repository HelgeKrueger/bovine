import logging

import werkzeug
from bovine_core.activitystreams import (
    build_actor,
)
from bovine_core.utils.crypto import content_digest_sha256
from quart import Blueprint, current_app, g, request
from quart_cors import route_cors

from bovine.types import ProcessingItem
from bovine.utils.server import ordered_collection_responder

cors_properties = {
    "allow_origin": ["http://localhost:8000"],
    "allow_methods": ["GET", "POST"],
    "allow_headers": ["Authorization", "Content-Type"],
}

activitypub = Blueprint("activitypub", __name__, url_prefix="/activitypub")

logger = logging.getLogger(__name__)


def has_authorization() -> bool:
    authorized_user = g.get("authorized_user")
    used_public_key = g.get("signature_result")

    return authorized_user or used_public_key


@activitypub.get("/<account_name>")
@route_cors(**cors_properties)
async def userinfo(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    user_info = await current_app.config["get_user"](account_name)

    if user_info and user_info.no_auth_fetch:
        logging.debug(f"Skipping signature check for user {account_name}")
    elif not has_authorization():
        return {"status": "http signature not valid"}, 401

    if not user_info:
        return {"status": "not found"}, 404

    domain = current_app.config["DOMAIN"]
    activitypub_profile_url = f"https://{domain}/activitypub/{user_info.name}"

    return (
        (
            build_actor(account_name, actor_type=user_info.actor_type)
            .with_account_url(activitypub_profile_url)
            .with_public_key(user_info.public_key)
            .build()
        ),
        200,
        {"content-type": "application/activity+json"},
    )


@activitypub.post("/<account_name>/inbox")
@route_cors(**cors_properties)
async def inbox(account_name: str) -> tuple[dict, int]:
    logger.debug("RECEIVED POST")
    current_app.add_background_task(handle_inbox, (account_name, request))

    return {"status": "processing"}, 202


async def handle_inbox(data) -> None:
    account_name, request = data
    raw_data = await request.get_data()
    digest = content_digest_sha256(raw_data)

    if not await current_app.config["validate_signature"](request, digest=digest):
        logger.warning("Incorrect http signature on post")
        return
    local_actor = await current_app.config["get_user"](account_name)
    inbox_item = ProcessingItem(raw_data)
    await local_actor.process_inbox_item(inbox_item, current_app.config["session"])


@activitypub.get("/<account_name>/outbox")
@route_cors(**cors_properties)
async def outbox(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    if not has_authorization():
        logger.warning("Invalid signature on get http request for outbox")
        return {"status": "request not signed"}, 401

    local_actor = await current_app.config["get_user"](account_name)
    arguments = {
        name: request.args.get(name)
        for name in ["first", "last", "min_id", "max_id"]
        if request.args.get(name) is not None
    }

    logger.debug(f"fetching outbox with arguments {arguments}")

    return await ordered_collection_responder(
        local_actor.get_outbox(),
        local_actor.item_count_for("outbox"),
        local_actor.items_for("outbox"),
        **arguments,
    )
