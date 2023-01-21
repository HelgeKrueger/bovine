from quart import Blueprint, redirect, request, current_app
import re
from urllib.parse import urlparse
import logging

from .models import OutboxEntry, Actor

outbox_blueprint = Blueprint("outbox", __name__)


@outbox_blueprint.get("/<username>/<uuid>")
async def element(username: str, uuid: str):
    request_path = urlparse(request.url).path

    if "Accept" not in request.headers:
        return redirect(request_path.replace("/testing_notes", ""))

    if not re.match(r"application/.*json", request.headers["Accept"]):
        print("redirecting")
        return redirect(request_path.replace("/testing_notes", ""))

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
