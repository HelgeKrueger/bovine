from quart import Blueprint

from .models import OutboxEntry, Actor

outbox_blueprint = Blueprint("outbox", __name__)


@outbox_blueprint.get("/<local_path>")
async def element(local_path: str):
    if "/" not in local_path:
        return {"status": "not found"}, 404

    username = local_path.split("/")[0]
    actor = await Actor.get_or_none(account=username)

    if actor is None:
        return {"status": "not found"}, 404

    entry = await OutboxEntry.get_or_none(actor=actor, local_path=local_path)

    if entry is None:
        return {"status": "not found"}, 404

    return entry.content, 200
