import logging
import os

import aiohttp
from quart import Quart
from tortoise.contrib.quart import register_tortoise

from bovine.server import default_configuration
from bovine.utils.http_signature import SignatureChecker
from bovine_tortoise.caches import build_public_key_fetcher
from bovine_tortoise.outbox_blueprint import outbox_blueprint
from bovine_tortoise.inbox import inbox_content_starting_from


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


app.config.update(
    {
        "DOMAIN": domain,
        "get_user": get_user,
        "data_store": TortoiseStore(),
        "domain_name": "mymath.rocks",
        "inbox_getter": inbox_content_starting_from,
    }
)

app.before_request(rewrite_activity_request)
app.register_blueprint(default_configuration)
app.register_blueprint(outbox_blueprint, url_prefix="/testing_notes")
app.register_blueprint(outbox_blueprint, url_prefix="/activitypub")
app.register_blueprint(html_blueprint)

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["bovine_tortoise.models", "aerich.models"],
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
