import re

import json

from bovine_core.activitystreams.objects import build_note
from bovine_core.activitystreams.activities import build_create

from bovine.types import ProcessingItem, LocalActor

from .replace_ids import replace_ids


async def test_replaces_id_of_note():
    local_actor = LocalActor("name", "url", "public_key", "private_key", "actor_type")
    note = build_note("account", "some_id", "uuid").build()

    item = ProcessingItem(json.dumps(note))
    result = await replace_ids(item, local_actor, None)
    result = result.get_data()

    assert re.match(
        r"url/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        result["id"],
    )


async def test_replaces_both_ids_in_activity():
    local_actor = LocalActor("name", "url", "public_key", "private_key", "actor_type")
    note = build_note("account", "some_id", "uuid").build()
    create = build_create(note).build()
    item = ProcessingItem(json.dumps(create))
    result = await replace_ids(item, local_actor, None)
    result = result.get_data()

    assert re.match(
        r"url/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/activity",
        result["id"],
    )
    assert re.match(
        r"url/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        result["object"]["id"],
    )
