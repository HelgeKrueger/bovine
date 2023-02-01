import logging
import re
from urllib.parse import urlparse

from quart import Blueprint, current_app, redirect, request

from .models import Actor, OutboxEntry

outbox_blueprint = Blueprint("outbox", __name__)


@outbox_blueprint.get("/<username>/<uuid>")
async def element(username: str, uuid: str):
    request_path = urlparse(request.url).path

    if "Accept" not in request.headers:
        new_path = request_path.replace("/activitypub", "")
        new_path = new_path.replace("/testing_notes", "")
        return redirect(new_path)

    if not re.match(r"application/.*json", request.headers["Accept"]):
        new_path = request_path.replace("/activitypub", "")
        new_path = new_path.replace("/testing_notes", "")
        return redirect(new_path)

    if not await current_app.config["validate_signature"](request, digest=None):
        logging.warn("Invalid signature on get http request")
        return {"status": "http signature not valid"}, 401

    actor = await Actor.get_or_none(account=username)

    if actor is None:
        return {"status": "not found"}, 404

    local_path = f"{username}/{uuid}"

    entry = await OutboxEntry.get_or_none(actor=actor, local_path=local_path)

    if entry is None:
        return {"status": "not found"}, 404

    return entry.content, 200
