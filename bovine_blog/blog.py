import os
import aiohttp
import logging
from quart import Quart
from tortoise.contrib.quart import register_tortoise

from bovine.server import default_configuration

from bovine_tortoise.outbox_blueprint import outbox_blueprint
from bovine.utils.http_signature import SignatureChecker
from bovine.clients import get_public_key

from .html import html_blueprint
from .build_store import build_get_user


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
    app.config.session = aiohttp.ClientSession()


def get_public_key_wrapper(key_id):
    return get_public_key(bovine_user, app.config.session, key_id)


signature_checker = SignatureChecker(get_public_key_wrapper)


app.config.update(
    {
        "DOMAIN": domain,
        "get_user": get_user,
        "validate_signature": signature_checker.validate_signature,
    }
)


app.register_blueprint(default_configuration)
app.register_blueprint(outbox_blueprint, url_prefix="/testing_notes")
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
