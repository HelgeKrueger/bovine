import asyncio
import uuid
from argparse import ArgumentParser

from rich.prompt import Prompt

from bovine.activitystreams.activities import build_create
from bovine.activitystreams.objects import build_note

from bovine_tortoise import ManagedDataStore
from bovine_tortoise.outbox import send_activity


async def publish_message(username, message):
    store = ManagedDataStore()
    await store.connect()

    local_user = await store.get_user(username)
    local_path = f"{username}/{str(uuid.uuid4())}"
    url = f"https://mymath.rocks/testing_notes/{local_path}"
    note = build_note(local_user.get_account(), url, message).as_public().build()
    create = build_create(note).build()

    await send_activity(local_user, create, local_path)

    await store.disconnect()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("username")

    message = Prompt.ask("Enter your message: ")

    args = parser.parse_args()

    asyncio.run(publish_message(args.username, message))
