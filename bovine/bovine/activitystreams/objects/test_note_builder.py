from .note_builder import NoteBuilder


def test_note_builder_basic():
    result = NoteBuilder("account", "content").build()

    assert result["@context"] == "https://www.w3.org/ns/activitystreams"
    assert result["type"] == "Note"
    assert result["content"] == "content"


def test_note_builder_hashtags():
    result = NoteBuilder("account", "content").with_hashtag("#tag1").build()

    assert isinstance(result["tag"], list)
    assert result["tag"][0] == {"name": "#tag1", "type": "Hashtag"}


def test_note_builder_hashtag_and_mention():
    result = (
        NoteBuilder("account", "content")
        .with_hashtag("#tag1")
        .with_mention("proto://server/path/mention")
        .build()
    )

    assert isinstance(result["tag"], list)
    assert result["tag"][0] == {"name": "#tag1", "type": "Hashtag"}
    assert result["tag"][1] == {
        "href": "proto://server/path/mention",
        "name": "proto://server/path/mention",
        "type": "Mention",
    }
    assert result["cc"] == ["proto://server/path/mention"]


def test_note_builder_cc():
    result = (
        NoteBuilder("account", "content", followers="account/followers")
        .as_public()
        .add_cc("user")
        .build()
    )

    assert set(result["cc"]) == {"account/followers", "user"}


def test_note_builder_cc_and_to():
    result = (
        NoteBuilder("account", "content", followers="account/followers")
        .as_public()
        .add_cc("user")
        .add_cc("user")
        .add_cc("to_user")
        .add_to("to_user")
        .build()
    )

    assert set(result["cc"]) == {"account/followers", "user"}
    assert "to_user" in result["to"]


def test_note_builder_for_reply():
    result = (
        NoteBuilder("account", "content")
        .with_conversation("conversation")
        .with_reply("reply_id")
        .build()
    )

    assert result["conversation"] == "conversation"
    assert result["inReplyTo"] == "reply_id"


def test_note_builder_for_source():
    result = NoteBuilder("account", "content").with_source("source", "format").build()

    assert result["source"] == {"content": "source", "mediaType": "format"}
