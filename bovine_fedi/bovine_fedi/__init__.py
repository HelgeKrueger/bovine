import logging
import os

from bovine_store.blueprint import bovine_store_blueprint
from bovine_store.config import configure_bovine_store
from bovine_user.config import configure_bovine_user
from bovine_user.server import bovine_user_blueprint
from quart import Quart
from quart_auth import AuthManager
from tortoise.contrib.quart import register_tortoise

from .build_store import build_get_user
from .config import TORTOISE_ORM, configure_bovine_fedi
from .server import default_configuration
from .server.authorization import add_authorization
from .server.endpoints import endpoints
from .utils import rewrite_activity_request
from .version import __version__

log_format = "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename=("bovine_debug.log"),
)
domain = os.environ.get("DOMAIN", "my_domain")
bovine_user, get_user = build_get_user(domain)

app = Quart(__name__)
AuthManager(app)


@app.before_serving
async def startup():
    await configure_bovine_fedi(app, bovine_user)
    await configure_bovine_user(app)
    await configure_bovine_store(app)


@app.after_serving
async def shutdown():
    await app.config["session"].close()


app.config.update(
    {
        "DOMAIN": domain,
        "get_user": get_user,
    }
)

app.before_request(rewrite_activity_request)
app.register_blueprint(default_configuration)
app.register_blueprint(bovine_user_blueprint, url_prefix="/bovine_user")
app.register_blueprint(endpoints, url_prefix="/endpoints")

bovine_store_blueprint.before_request(add_authorization)
app.register_blueprint(bovine_store_blueprint, url_prefix="/objects")

register_tortoise(
    app,
    db_url=TORTOISE_ORM["connections"]["default"],
    modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    generate_schemas=False,
)
