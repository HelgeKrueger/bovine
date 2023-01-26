import os
import json
import logging

import werkzeug
from quart import Blueprint, current_app, request
from quart_cors import route_cors

from bovine.utils.crypto import content_digest_sha256

activitypub_client = Blueprint(
    "activitypub_client", __name__, url_prefix="/activitypub"
)

logger = logging.getLogger("ap-c2s")


access_token = os.environ.get("ACCESS_TOKEN", None)


# FIXME This does not implement anything good yet
@activitypub_client.get("/<account_name>/inbox_tmp")
@route_cors(allow_origin=["http://localhost:8000"], allow_methods=["GET"])
async def inbox_get(account_name: str):
    authorization_header = request.headers.get("Authorization", None)

    if not authorization_header or not authorization_header.startswith("Bearer "):
        logger.warning(f"GET on inbox for {account_name} without authorization")
        return {"status": "access denied"}, 401

    token = authorization_header.removeprefix("Bearer ")

    if token != access_token:
        logger.warning(f"GET on inbox for {account_name} with incorrect authorization")
        return {"status": "access denied"}, 401

    logger.info("Fetching inbox with GET")
    minimal_id = int(request.args.get("min_id", 0))

    result = await current_app.config["inbox_getter"](account_name, minimal_id)

    if result is None:
        result = {}

    return result, 200


@activitypub_client.post("/<account_name>/outbox")
@activitypub_client.post("/<account_name>/outbox_tmp")
@route_cors(allow_origin=["http://localhost:8000"], allow_methods=["POST"])
async def post_outbox(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    raw_data = await request.get_data()

    authorization_header = request.headers.get("Authorization", None)

    if authorization_header:
        if not authorization_header or not authorization_header.startswith("Bearer "):
            logger.warning(
                f"POST on outbox for {account_name} with incorrect authorization"
            )
            return {"status": "access denied"}, 401

        token = authorization_header.removeprefix("Bearer ")

        if token != access_token:
            logger.warning(
                f"POST on outbox for {account_name} with incorrect authorization"
            )
            return {"status": "access denied"}, 401
        local_user = await current_app.config["get_user"](account_name)
    else:
        digest = content_digest_sha256(raw_data)

        used_key_url = await current_app.config["validate_signature"](
            request, digest=digest
        )

        if used_key_url is None:
            logger.warning("Invalid signature on get http request for outbox")
            return {"status": "request not signed"}, 401

        local_user = await current_app.config["get_user"](account_name)

        if local_user.get_public_key_url() != used_key_url:
            logger.warning(f"Attempt to post with incorrect key {used_key_url}")
            return {"status": "request not signed"}, 401

    await local_user.add_outbox_item(
        current_app.config["session"], json.loads(raw_data)
    )

    return {"status": "success"}, 200
