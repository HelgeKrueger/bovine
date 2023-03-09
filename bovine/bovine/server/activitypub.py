import logging

import werkzeug
from bovine_core.activitystreams import (
    build_actor,
)
from quart import Blueprint, current_app, g
from quart_cors import route_cors

from bovine_core.types import Visibility
from bovine_core.activitystreams import build_ordered_collection

cors_properties = {
    "allow_origin": ["http://localhost:8000"],
    "allow_methods": ["GET", "POST"],
    "allow_headers": ["Authorization", "Content-Type", "Last-Event-Id"],
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

    if not user_info:
        return {"status": "not found"}, 404

    domain = current_app.config["DOMAIN"]
    activitypub_profile_url = f"https://{domain}/activitypub/{user_info.name}"

    visibility = Visibility.WEB

    if has_authorization():
        visibility = Visibility.PUBLIC

    if (
        g.get("authorized_user") == account_name
        or g.get("signature_result") == user_info.get_public_key_url()
    ):
        visibility = Visibility.OWNER

    return (
        (
            build_actor(account_name, actor_type=user_info.actor_type)
            .with_account_url(activitypub_profile_url)
            .with_public_key(user_info.public_key)
            .build(visibility=visibility)
        ),
        200,
        {"content-type": "application/activity+json"},
    )


@activitypub.post("/<account_name>/inbox")
@route_cors(**cors_properties)
async def inbox(account_name: str) -> tuple[dict, int]:
    return {"status": "not implemented"}, 501


@activitypub.get("/<account_name>/outbox")
@route_cors(**cors_properties)
async def outbox(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    if not has_authorization():
        logger.warning("Invalid signature on get http request for outbox")
        return {"status": "request not signed"}, 401

    local_actor = await current_app.config["get_user"](account_name)
    return build_ordered_collection(local_actor.get_outbox()).with_count(0).build(), 200
