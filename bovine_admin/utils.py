from markdown import Markdown

from bovine.activitystreams.objects import build_note
from bovine.activitystreams.activities import build_create


def build_create_note_activity_from_data_base_case(
    account_url: str, post_url: str, data: dict
) -> dict:

    source = data["content"]
    md = Markdown(extensions=["mdx_math"])
    message = md.convert(source)

    builder = build_note(account_url, post_url, message).as_public()

    for tag in data.get("hashtags", []):
        builder = builder.with_hashtag(tag)
    for mention in data.get("mentions", []):
        builder = builder.with_mention(mention)
    for cc in data.get("previous_cc", []):
        builder = builder.add_cc(cc)

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

    return create
