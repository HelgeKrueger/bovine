import logging

import werkzeug
from bovine.activitystreams import build_actor, build_ordered_collection
from bovine.types import Visibility
from quart import Blueprint, current_app

activitypub = Blueprint("activitypub", __name__, url_prefix="/activitypub")

logger = logging.getLogger(__name__)


@activitypub.get("/<account_name>")
async def userinfo(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    user_info = await current_app.config["get_user"](account_name)

    if not user_info and account_name != "bovine":
        return {"status": "not found"}, 404

    domain = current_app.config["DOMAIN"]
    activitypub_profile_url = f"https://{domain}/activitypub/{user_info.name}"

    visibility = Visibility.WEB

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
async def inbox(account_name: str) -> tuple[dict, int]:
    return {"status": "not implemented"}, 501


@activitypub.get("/<account_name>/outbox")
async def outbox(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    local_actor = await current_app.config["get_user"](account_name)
    return build_ordered_collection(local_actor.get_outbox()).with_count(0).build(), 200
