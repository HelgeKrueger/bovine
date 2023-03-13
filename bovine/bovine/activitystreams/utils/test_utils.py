from bovine.activitystreams.objects import build_note

from . import actor_for_object, is_public, recipients_for_object


def test_get_recipients():
    note = (
        build_note("account", "url", "content")
        .as_public()
        .add_cc("cc")
        .add_to("to")
        .add_cc("same")
        .add_to("same")
        .build()
    )

    recipients = recipients_for_object(note)

    assert recipients == {
        "account/followers",
        "https://www.w3.org/ns/activitystreams#Public",
        "cc",
        "to",
        "same",
    }


def test_is_public():
    note = build_note("account", "url", "content").as_public().build()
    assert is_public(note)

    note = build_note("account", "url", "content").build()
    assert not is_public(note)

    note = build_note("account", "url", "content").add_cc("someone").build()
    assert not is_public(note)

    note = build_note("account", "url", "content").as_unlisted().build()
    assert is_public(note)

    note = build_note("account", "url", "content").add_to("as:Public").build()
    note["to"] = "as:Public"
    assert is_public(note)


def test_actor_for_object():
    assert actor_for_object({}) == "__NO__ACTOR__"
    assert actor_for_object({"actor": "alice"}) == "alice"
    assert actor_for_object({"actor": {"id": "alice"}}) == "alice"
    assert actor_for_object({"actor": {}}) == "__NO__ACTOR__"
    assert actor_for_object({"attributedTo": "alice"}) == "alice"
    assert actor_for_object({"attributedTo": {"id": "alice"}}) == "alice"
    assert actor_for_object({"attributedTo": {}}) == "__NO__ACTOR__"
