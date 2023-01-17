import os

from quart import Quart
from tortoise.contrib.quart import register_tortoise

from bovine.server import default_configuration
from bovine_tortoise import (
    ManagedDataStore,
    default_inbox_processors,
    default_outbox,
)
from bovine_tortoise.outbox_blueprint import outbox_blueprint


app = Quart(__name__)

domain = os.environ["DOMAIN"]

app.config.update(
    {
        "DOMAIN": domain,
    }
)
app.config.data_store = ManagedDataStore(
    inbox_processors=default_inbox_processors, outbox_handlers=default_outbox
)
app.register_blueprint(default_configuration)
app.register_blueprint(outbox_blueprint, url_prefix="/testing_notes")
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["bovine_tortoise.models"]},
    generate_schemas=False,
)
