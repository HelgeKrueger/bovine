import logging

from quart import Quart
from quart_auth import AuthManager
from tortoise.contrib.quart import register_tortoise

from bovine_user.config import configure_bovine_user
from bovine_user.server import bovine_user_blueprint

logging.basicConfig(level=logging.INFO)

app = Quart(__name__)
AuthManager(app)

app.register_blueprint(bovine_user_blueprint)


TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": [
                "bovine_user.models",
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


@app.before_serving
async def startup():
    await configure_bovine_user(app)


if __name__ == "__main__":
    app.run()
