import re

from bovine.activitystreams.objects import build_note

from .create_builder import CreateBuilder


def test_basic_build():
    result = CreateBuilder({"a": "message"}).build()

    assert "https://www.w3.org/ns/activitystreams" in result["@context"]
    assert result["type"] == "Create"
    assert result["id"] is None
    assert result["actor"] is None
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", result["published"])


def test_basic_build_as_unlisted():
    result = (
        CreateBuilder({"a": "message"}).with_account("account").as_unlisted().build()
    )

    assert result["to"] == ["account/followers"]
    assert result["cc"] == ["https://www.w3.org/ns/activitystreams#Public"]


def test_copies_from_note_if_available():
    note = build_note("account", "url", "content").as_public().build()

    result = CreateBuilder(note).build()

    assert result["actor"] == "account"
