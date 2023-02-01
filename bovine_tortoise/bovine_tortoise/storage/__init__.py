from quart import Blueprint, Response, current_app

storage_blueprint = Blueprint("storage_blueprint", __name__, url_prefix="/storage")


@storage_blueprint.get("/<name>")
async def get_from_storage(name):
    try:
        obj = await current_app.config["object_storage"].get_object(name)

    except Exception as e:
        print(e)

    if obj is None:
        return {"status": "not found"}, 404

    return Response(obj.data, mimetype="image/png")
