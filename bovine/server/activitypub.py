from quart import Blueprint, current_app, request

from bovine.activitystreams import build_actor, build_outbox
from bovine.processors import InboxItem

activitypub = Blueprint("activitypub", __name__, url_prefix="/activitypub")


@activitypub.get("/<account_name>")
async def userinfo(account_name: str) -> dict:
    user_info = await current_app.config.data_store.get_user(account_name)

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
async def inbox(account_name: str) -> dict:
    headers = request.headers
    raw_data = await request.get_data()

    if "signature" not in headers:
        return {"status": "request not signed"}, 401

    local_user = await current_app.config.data_store.get_user(account_name)
    inbox_item = InboxItem(dict(request.headers), raw_data)

    current_app.add_background_task(local_user.process_inbox_item, inbox_item)

    return {"status": "processing"}, 202


@activitypub.get("/<account_name>/outbox")
async def outbox(account_name: str) -> dict:
    domain = current_app.config["DOMAIN"]
    outbox_url = f"https://{domain}/activitypub/{account_name}/outbox"
    local_user = await current_app.config.data_store.get_user(account_name)

    count = await local_user.outbox_item_count()
    items = await local_user.outbox_items()

    return build_outbox(outbox_url).with_count(count).with_items(items).build()
