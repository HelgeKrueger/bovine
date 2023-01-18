from quart import Blueprint, render_template

from bovine_tortoise.models import OutboxEntry, Actor

html_blueprint = Blueprint("html_blueprint", __name__)


def extract_content(activity):
    obj = activity["object"]
    return obj["content"]


@html_blueprint.get("/")
async def index():
    actor = await Actor.get_or_none(account="helge")
    entries = await OutboxEntry.filter(actor=actor).all()

    contents = [extract_content(entry.content) for entry in entries][::-1]

    return await render_template("index.html", contents=contents)


@html_blueprint.get("/<username>")
@html_blueprint.get("/<username>/")
async def user(username):
    actor = await Actor.get_or_none(account="helge")
    entries = await OutboxEntry.filter(actor=actor).all()

    contents = [extract_content(entry.content) for entry in entries][::-1]

    return await render_template("index.html", contents=contents)


@html_blueprint.get("/<username>/<uuid>")
async def post(username, uuid):
    actor = await Actor.get_or_none(account=username)

    if actor is None:
        return {"status": "not found"}, 404

    local_path = f"{username}/{uuid}"

    entry = await OutboxEntry.get_or_none(actor=actor, local_path=local_path)

    if entry is None:
        return {"status": "not found"}, 404

    content = extract_content(entry.content)

    return await render_template("post.html", content=content)
