import logging
import re

from quart import redirect, request

logger = logging.getLogger("rewrite")


from urllib.parse import urlparse

from tortoise import Tortoise


async def init(db_url: str = "sqlite://db.sqlite3") -> None:
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["bovine_fedi.models", "bovine_user.models"]},
    )
    await Tortoise.generate_schemas()

    return None


def determine_local_path_from_activity_id(activity_id):
    local_path = urlparse(activity_id).path
    return local_path


async def rewrite_activity_request():
    accept_header = request.headers.get("accept", "*/*")

    if request.method == "get":
        if any(
            request.path.startswith(url) for url in ["/activitypub", "/testing_notes"]
        ):
            if not re.match(r"application/.*json", accept_header):
                new_path = request.path.replace(r"/activitypub", "")
                new_path = new_path.replace(r"/testing_notes", "")
                logging.info(f"Rewrote path to {new_path}")
                return redirect(new_path)

    return


async def update_id(data, retriever, store):
    data["id"] = await store.id_generator()
    if "object" in data and isinstance(data["object"], dict):
        obj_in_store = await store.retrieve(retriever, data["object"]["id"])
        if not obj_in_store:
            data["object"]["id"] = await store.id_generator()

    return data
