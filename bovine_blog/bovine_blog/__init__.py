import logging
import os

import aiohttp
from bovine.server import default_configuration
from bovine.utils.queue_manager import QueueManager
from bovine_core.utils.signature_checker import SignatureChecker
from bovine_store.store import ObjectStore
from bovine_tortoise.caches import build_public_key_fetcher
from bovine_tortoise.outbox_blueprint import outbox_blueprint
from bovine_tortoise.storage import storage_blueprint
from bovine_tortoise.storage.storage import Storage
from quart import Quart
from tortoise.contrib.quart import register_tortoise

from .build_store import build_get_user
from .html import html_blueprint
from .stores.tortoise import TortoiseStore
from .utils import rewrite_activity_request

log_format = "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename=("debug.log"),
)
domain = os.environ.get("DOMAIN", "my_domain")
bovine_user, get_user = build_get_user(domain)

app = Quart(__name__)


@app.before_serving
async def startup():
    session = aiohttp.ClientSession()
    public_key_fetcher = build_public_key_fetcher(session, bovine_user)
    signature_checker = SignatureChecker(public_key_fetcher)

    app.config["session"] = session
    app.config["validate_signature"] = signature_checker.validate_signature

    app.config["queue_manager"] = QueueManager()
    app.config["object_store"] = ObjectStore()


async def account_name_or_none_for_token(token):
    access_token = os.environ.get("ACCESS_TOKEN", None)
    if token == access_token:
        return "helge"
    return None


app.config.update(
    {
        "DOMAIN": domain,
        "get_user": get_user,
        "data_store": TortoiseStore(),
        "domain_name": "mymath.rocks",
        "account_name_or_none_for_token": account_name_or_none_for_token,
        "object_storage": Storage(),
    }
)

app.before_request(rewrite_activity_request)
app.register_blueprint(default_configuration)
app.register_blueprint(outbox_blueprint, url_prefix="/testing_notes")
app.register_blueprint(outbox_blueprint, url_prefix="/activitypub")
app.register_blueprint(html_blueprint)
app.register_blueprint(storage_blueprint)

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": [
                "bovine_tortoise.models",
                "bovine_store.models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    db_url=TORTOISE_ORM["connections"]["default"],
    modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    generate_schemas=False,
)
