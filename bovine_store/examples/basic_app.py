import logging

from quart import Quart, g
from quart_auth import AuthManager
from tortoise.contrib.quart import register_tortoise

from bovine_store.store.collection import add_to_collection
from bovine_store.config import configure_bovine_store
from bovine_store.blueprint import bovine_store_blueprint
from bovine_store.collection import collection_response

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

    await add_to_collection("/endpoint", result[0]["id"])

    print()
    print(f"Open {result[0]['id']} to see a document in the store")
    print("Open http://localhost:5000/collection to see a collection")
    print()


@app.before_request
async def add_actor():
    g.retriever = "owner"
    # g.retriever = None


app.register_blueprint(bovine_store_blueprint, url_prefix="/objects")


@app.get("/collection")
async def collection():
    return await collection_response("/endpoint")


if __name__ == "__main__":
    app.run()
