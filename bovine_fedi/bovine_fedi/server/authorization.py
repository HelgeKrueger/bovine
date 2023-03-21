import logging
import re

from bovine.utils.crypto import content_digest_sha256
from quart import current_app, g, request
from quart_auth import current_user

logger = logging.getLogger(__name__)


def is_get():
    return re.match(r"^get$", request.method, re.IGNORECASE)


def is_post():
    return re.match(r"^post$", request.method, re.IGNORECASE)


async def compute_signature_result() -> str | None:
    if request.method.lower() == "get":
        return await current_app.config["validate_signature"](request, digest=None)

    if is_post():
        raw_data = await request.get_data()
        digest = content_digest_sha256(raw_data)
        return await current_app.config["validate_signature"](request, digest=digest)

    return None


async def add_authorization():
    g.signature_result = await compute_signature_result()

    if g.signature_result:
        g.retriever = g.signature_result.split("#")[0]
    elif await current_user.is_authenticated:
        manager = current_app.config["bovine_user_manager"]
        _, actor = await manager.get_activity_pub(current_user.auth_id)
        if actor:
            g.retriever = actor.build()["id"]
        else:
            g.retriever = "NONE"
            logger.warning("Unknown auth id %s", current_user.auth_id)
    else:
        g.retriever = "NONE"
