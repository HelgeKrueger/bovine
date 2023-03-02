import logging

from quart import Quart, g
from quart_auth import AuthManager
from tortoise.contrib.quart import register_tortoise

from bovine_store.config import configure_bovine_store

logging.basicConfig(level=logging.INFO)

app = Quart(__name__)
AuthManager(app)

# app.register_blueprint(server)


TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": [
                "bovine_store.models",
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
    await configure_bovine_store(app)

    result = await app.config["bovine_store"].store_local(
        "owner",
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Like",
        },
    )

    print()
    print(f"Open {result[0]['id']} to see a document in the store")
    print()


@app.before_request
async def add_actor():
    g.actor_id = "owner"


if __name__ == "__main__":
    app.run()
