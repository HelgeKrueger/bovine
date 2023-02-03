import json

from bovine.types import InboxItem, LocalUser
from bovine_tortoise.models import Actor


async def create_actor_and_local_user():
    actor = await Actor.create(
        account="name",
        url="/activitypub/name",
        actor_type="type",
        private_key="private_key",
        public_key="public_key",
    )

    local_user = LocalUser(
        "name", "/activitypub/name", "public_key", "private_key", "actor_type"
    )

    return actor, local_user


def build_inbox_item_from_json(json_file_name):
    with open(json_file_name, "r") as f:
        return InboxItem(f.read())


def get_activity_from_json(json_file_name):
    with open(json_file_name, "r") as f:
        return json.load(f)


fake_post_headers = {
    "Content-Type": "application/activity+json",
    "Signature": "signature",
    "date": "date",
    "host": "host",
    "digest": "XXXxx",
}

fake_get_headers = {
    "Accept": "application/activity+json",
    "date": "date",
    "host": "host",
}
