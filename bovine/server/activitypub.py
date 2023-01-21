import logging
from urllib.parse import urlparse
import re

import werkzeug
from quart import Blueprint, current_app, request, redirect

from bovine.activitystreams import build_actor, build_outbox
from bovine.types import InboxItem
from bovine.utils.crypto import content_digest_sha256

activitypub = Blueprint("activitypub", __name__, url_prefix="/activitypub")

logger = logging.getLogger("activitypub")


@activitypub.get("/<account_name>")
async def userinfo(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    request_path = urlparse(request.url).path

    if "Accept" not in request.headers:
        return redirect(request_path.replace("/activitypub", ""))

    if not re.match(r"application/.*json", request.headers["Accept"]):
        print("redirecting")
        return redirect(request_path.replace("/activitypub", ""))

    if not await current_app.config["validate_signature"](request, digest=None):
        logger.warning("Invalid signature on get http request for account")
        return {"status": "http signature not valid"}, 401

    user_info = await current_app.config["get_user"](account_name)

    if not user_info:
        return {"status": "not found"}, 404

    domain = current_app.config["DOMAIN"]
    activitypub_profile_url = f"https://{domain}/activitypub/{user_info.name}"

    return (
        build_actor(account_name, actor_type=user_info.actor_type)
        .with_account_url(activitypub_profile_url)
        .with_public_key(user_info.public_key)
        .build()
    )


@activitypub.post("/<account_name>/inbox")
async def inbox(account_name: str) -> tuple[dict, int]:
    current_app.add_background_task(handle_inbox, (account_name, request))

    return {"status": "processing"}, 202


async def handle_inbox(data) -> None:
    account_name, request = data
    raw_data = await request.get_data()
    digest = content_digest_sha256(raw_data)

    if not await current_app.config["validate_signature"](request, digest=digest):
        logger.warning("Incorrect http signature on post")
        return
    local_user = await current_app.config["get_user"](account_name)
    inbox_item = InboxItem(dict(request.headers), raw_data)
    await local_user.process_inbox_item(inbox_item)


@activitypub.get("/<account_name>/outbox")
async def outbox(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    request_path = urlparse(request.url).path

    if "Accept" not in request.headers:
        return redirect(request_path.replace("/activitypub", ""))

    if not re.match(r"application/.*json", request.headers["Accept"]):
        print("redirecting")
        return redirect(request_path.replace("/activitypub", ""))

    if not await current_app.config["validate_signature"](request, digest=None):
        logger.warning("Invalid signature on get http request for outbox")
        return {"status": "request not signed"}, 401

    domain = current_app.config["DOMAIN"]
    outbox_url = f"https://{domain}/activitypub/{account_name}/outbox"
    local_user = await current_app.config["get_user"](account_name)

    count = await local_user.outbox_item_count()
    items = await local_user.outbox_items()

    return build_outbox(outbox_url).with_count(count).with_items(items).build()
