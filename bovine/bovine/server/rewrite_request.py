import logging
import os
import re

from bovine_core.utils.crypto import content_digest_sha256
from quart import current_app, g, redirect, request

from bovine.utils.parsers.accept_header import is_activity_request

logger = logging.getLogger(__name__)


access_token = os.environ.get("ACCESS_TOKEN", None)


def is_get():
    return re.match(r"^get$", request.method, re.IGNORECASE)


def is_post():
    return re.match(r"^post$", request.method, re.IGNORECASE)


def is_activity_pub():
    if is_get():
        accept_header = request.headers.get("accept", "*/*")
        logger.debug(f"obtained accept header '{accept_header}'")
        if accept_header == "text/event-stream":
            return True

        return is_activity_request(accept_header)

    if is_post():
        # content_type = request.headers.get("content-type", "*/*")
        # return is_activity_request(content_type)
        # will support posts with form encoded data for images.
        return True

    if re.match(r"^options$", request.method, re.IGNORECASE):
        return True

    return False


async def compute_signature_result() -> str | None:
    if is_get():
        return await current_app.config["validate_signature"](request, digest=None)

    if is_post():
        raw_data = await request.get_data()
        digest = content_digest_sha256(raw_data)
        return await current_app.config["validate_signature"](request, digest=digest)

    return None


async def retrieve_authorizated_user() -> str | None:
    authorization_header = request.headers.get("Authorization", None)

    if not authorization_header:
        return None

    if not authorization_header.startswith("Bearer "):
        logger.warning(
            f"Non Bearer Authorization used {authorization_header} for {request.path}"
        )
        return None

    token = authorization_header.removeprefix("Bearer ")

    return await current_app.config["account_name_or_none_for_token"](token)


async def rewrite_activity_request():
    if request.path == "/activitypub/bovine":
        return

    new_request_path = request.path.removeprefix("/activitypub")

    if is_activity_pub():
        new_request_path = "/activitypub" + new_request_path
        await add_authorization_to_request()

    if request.path != new_request_path:
        logger.info(f"Rewrote {request.path} to {new_request_path}")
        request.path = new_request_path
        return redirect(new_request_path)


async def add_authorization_to_request():
    g.signature_result = await compute_signature_result()
    g.authorized_user = await retrieve_authorizated_user()
    logger.info(f"Obtained {g.signature_result} and {g.authorized_user}")
