import os

from quart import Quart
from tortoise.contrib.quart import register_tortoise

from bovine.server import default_configuration
from bovine_tortoise import (
    ManagedDataStore,
    default_inbox_processors,
    default_outbox,
)
from bovine.processors.dismiss_delete import dismiss_delete
from bovine_tortoise.outbox_blueprint import outbox_blueprint
from bovine.utils.http_signature import SignatureChecker
from bovine.clients import get_public_key

from .html import html_blueprint

import logging


app = Quart(__name__)

signature_checker = SignatureChecker(get_public_key)


log_format = "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename=("debug.log"),
)

app = Quart(__name__)

domain = os.environ.get("DOMAIN", "my_domain")

app.config.update(
    {
        "DOMAIN": domain,
    }
)
app.config.validate_signature = signature_checker.validate_signature


async def on_delete(local_user, item):
    item.dump()


inbox_processors = [dismiss_delete(on_delete)] + default_inbox_processors
app.config.data_store = ManagedDataStore(
    inbox_processors=inbox_processors, outbox_handlers=default_outbox
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
