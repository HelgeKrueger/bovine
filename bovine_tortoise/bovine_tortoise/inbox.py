from .models import Actor, InboxEntry


async def inbox_content_starting_from(username: str, minimal_id: int) -> list:
    actor = await Actor.get_or_none(account=username)
    entries = await InboxEntry.filter(actor=actor, read=True, id__gt=minimal_id).all()

    contents = [[entry.id, entry.content] for entry in entries]

    return contents[::-1]
