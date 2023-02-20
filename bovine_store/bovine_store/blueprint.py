from quart import Blueprint, g

bovine_store_blueprint = Blueprint("bovine_store", __name__)


@bovine_store_blueprint.get("/<uuid:uuid>")
def retrieve_from_store(uuid):
    print(uuid)
    print(g.actor_url)

    return "success"
