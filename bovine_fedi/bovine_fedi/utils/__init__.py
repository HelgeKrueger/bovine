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


from bovine_fedi.types import LocalActor

__version__ = "0.0.4"


def get_bovine_user(
    domain: str,
) -> LocalActor:
    server_public_key, server_private_key = get_server_keys()

    url = f"https://{domain}/activitypub/bovine"

    bovine_user = LocalActor(
        "bovine",
        url,
        server_public_key,
        server_private_key,
        "Application",
        no_auth_fetch=True,
    ).set_inbox_process(dump_incoming_inbox_to_stdout)

    return bovine_user


import os

from bovine_core.utils.crypto import generate_public_private_key


async def dump_incoming_inbox_to_stdout(local_user, result):
    result.dump()
    return local_user


def get_server_keys():
    public_key_path = ".files/server_public_key.pem"
    private_key_path = ".files/server_private_key.pem"

    return get_public_private_key_from_files(public_key_path, private_key_path)


def get_public_private_key_from_files(public_key_path, private_key_path):
    public_key = None
    private_key = None

    if os.path.exists(public_key_path):
        with open(public_key_path) as f:
            public_key = f.read()
    if os.path.exists(private_key_path):
        with open(private_key_path) as f:
            private_key = f.read()

    if public_key and private_key:
        return public_key, private_key

    public_key_pem, private_key_pem = generate_public_private_key()

    if not os.path.exists(".files"):
        os.mkdir(".files")

    with open(public_key_path, "w") as f:
        f.write(public_key_pem)

    with open(private_key_path, "w") as f:
        f.write(private_key_pem)

    return public_key_pem, private_key_pem
