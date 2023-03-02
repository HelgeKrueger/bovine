import tomli
import aiohttp
import uuid

from .blueprint import bovine_store_blueprint
from .store import ObjectStore


async def configure_bovine_store(app):
    with open("bovine_config.toml", "rb") as fp:
        config_data = tomli.load(fp)

    if "session" not in app.config:
        app.config["session"] = aiohttp.ClientSession()

    host = config_data["bovine"]["host"]
    app.config["host"] = host

    async def id_generator():
        return host + "/objects/" + str(uuid.uuid4())

    app.config["bovine_store"] = ObjectStore(id_generator=id_generator)

    app.register_blueprint(bovine_store_blueprint, url_prefix="/objects")
