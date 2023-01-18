from quart import Quart, request
from tortoise.contrib.quart import register_tortoise
import aiohttp
import uuid
import json

from markdown import Markdown

from bovine.activitystreams.objects import build_note
from bovine.activitystreams.activities import build_create

from bovine_tortoise.models import Actor, InboxEntry, Following, Follower
from bovine_tortoise.actions import follow
from bovine_tortoise import ManagedDataStore
from bovine_tortoise.outbox import send_activity

import logging

log_format = "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename=("debug_admin.log"),
)


app = Quart(__name__)
username = "helge"


@app.before_serving
async def startup():
    app.client = aiohttp.ClientSession()


@app.get("/")
async def index():
    actor = await Actor.get_or_none(account=username)
    entries = await InboxEntry.filter(actor=actor).all()

    contents = [[entry.id, entry.content] for entry in entries]

    return contents[::-1]


@app.get("/follow")
async def get_follow():
    actor = await Actor.get_or_none(account=username)
    following = await Following.filter(actor=actor).all()
    follower = await Follower.filter(actor=actor).all()

    following_list = [x.account for x in following]
    follower_list = [x.account for x in follower]

    return {"follower": follower_list, "following": following_list}


@app.route("/add_follow", methods=["POST"])
async def add_follow():
    store = ManagedDataStore()
    local_user = await store.get_user(username)
    data = await request.get_json()

    remote_account = data["account"]

    print(remote_account)

    await follow(app.client, local_user, remote_account)

    print("done")

    return {}


@app.route("/cleanup")
async def cleanup_timeline():
    max_id = request.args.get("max_id")
    actor = await Actor.get_or_none(account=username)
    await InboxEntry.filter(actor=actor).filter(id__lt=max_id).delete()

    return {"status": "done"}


async def send_activity_wrapper(list_of_args):
    await send_activity(*list_of_args)


@app.route("/post", methods=["POST"])
async def handle_post():
    store = ManagedDataStore()
    local_user = await store.get_user(username)
    data = await request.get_json()

    local_path = f"{username}/{str(uuid.uuid4())}"
    url = f"https://mymath.rocks/testing_notes/{local_path}"

    source = data["content"]
    md = Markdown(extensions=["mdx_math"])

    message = md.convert(source)

    builder = build_note(local_user.get_account(), url, message).as_public()

    for tag in data["hashtags"]:
        builder = builder.with_hashtag(tag)

    if "conversation" in data:
        builder = builder.with_conversation(data["conversation"])
    if "reply_to_id" in data:
        builder = builder.with_reply(data["reply_to_id"])
    if "reply_to_atom_uri" in data:
        builder = builder.with_reply_to_atom_uri(data["reply_to_atom_uri"])
    if "reply_to_actor" in data:
        builder = builder.add_cc(data["reply_to_actor"])

    note = builder.build()

    create = build_create(note).build()

    logging.info("Posting")
    logging.info(json.dumps(create))

    app.add_background_task(send_activity_wrapper, (local_user, create, local_path))

    return {}


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["bovine_tortoise.models"]},
    generate_schemas=False,
)
