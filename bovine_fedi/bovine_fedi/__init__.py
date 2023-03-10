import logging
import os

import aiohttp
from bovine.utils.signature_checker import SignatureChecker
from bovine_store.blueprint import bovine_store_blueprint
from bovine_store.config import configure_bovine_store
from bovine_user.config import configure_bovine_user
from bovine_user.server import bovine_user_blueprint
from quart import Quart
from quart_auth import AuthManager
from tortoise.contrib.quart import register_tortoise

from .build_store import build_get_user
from .caches import build_public_key_fetcher
from .endpoints import add_authorization, endpoints
from .server import default_configuration
from .storage import storage_blueprint
from .storage.storage import Storage
from .utils import rewrite_activity_request
from .utils.queue_manager import QueueManager
from .version import __version__

log_format = "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename=("debug.log"),
)
domain = os.environ.get("DOMAIN", "my_domain")
bovine_user, get_user = build_get_user(domain)

app = Quart(__name__)
AuthManager(app)


@app.before_serving
async def startup():
    session = aiohttp.ClientSession()
    public_key_fetcher = build_public_key_fetcher(session, bovine_user)
    signature_checker = SignatureChecker(public_key_fetcher)

    app.config["session"] = session
    app.config["validate_signature"] = signature_checker.validate_signature

    app.config["queue_manager"] = QueueManager()

    await configure_bovine_user(app)
    await configure_bovine_store(app)


@app.after_serving
async def shutdown():
    await app.config["session"].close()


async def account_name_or_none_for_token(token):
    access_token = os.environ.get("ACCESS_TOKEN", None)
    if token == access_token:
        return "helge"
    return None


app.config.update(
    {
        "DOMAIN": domain,
        "get_user": get_user,
        "domain_name": "mymath.rocks",
        "account_name_or_none_for_token": account_name_or_none_for_token,
        "object_storage": Storage(),
    }
)

app.before_request(rewrite_activity_request)
app.register_blueprint(default_configuration)
app.register_blueprint(storage_blueprint)
app.register_blueprint(bovine_user_blueprint, url_prefix="/bovine_user")
app.register_blueprint(endpoints, url_prefix="/endpoints")

bovine_store_blueprint.before_request(add_authorization)
app.register_blueprint(bovine_store_blueprint, url_prefix="/objects")


TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": [
                "bovine_fedi.models",
                "bovine_store.models",
                "bovine_user.models",
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
