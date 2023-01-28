from quart import Quart, request
from quart_cors import route_cors, cors

from tortoise.contrib.quart import register_tortoise

from bovine_tortoise.storage import storage_blueprint
from bovine_tortoise.storage.storage import Storage

from bovine_blog import TORTOISE_ORM

app = Quart(__name__)
app.config["object_storage"] = Storage()
app.register_blueprint(storage_blueprint)
app = cors(app)


@route_cors(allow_origin="*")
@app.post("/add")
async def my_post():
    await request.get_data(parse_form_data=True)
    files = await request.files
    await app.config["object_storage"].add_object("image", files["image"].read())

    return "success", 200


register_tortoise(
    app,
    db_url=TORTOISE_ORM["connections"]["default"],
    modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    generate_schemas=False,
)


if __name__ == "__main__":
    app.run()
