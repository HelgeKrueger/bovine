from .note_builder import NoteBuilder


def test_note_builder_basic():
    result = NoteBuilder("account", "url", "content").build()

    assert result["@context"] == "https://www.w3.org/ns/activitystreams"
    assert result["type"] == "Note"
    assert result["content"] == "content"


def test_note_builder_hashtags():
    result = NoteBuilder("account", "url", "content").with_hashtag("#tag1").build()

    assert isinstance(result["tag"], list)
    assert result["tag"][0] == {"name": "#tag1", "type": "Hashtag"}


def test_note_builder_cc():
    result = NoteBuilder("account", "url", "content").as_public().add_cc("user").build()

    assert result["cc"] == ["account/followers", "user"]


def test_note_builder_for_reply():
    result = (
        NoteBuilder("account", "url", "content")
        .with_conversation("conversation")
        .with_reply("reply_id")
        .with_reply_to_atom_uri("atom_uri")
        .build()
    )

    assert result["conversation"] == "conversation"
    assert result["inReplyTo"] == "reply_id"
    assert result["inReplyToAtomUri"] == "atom_uri"
