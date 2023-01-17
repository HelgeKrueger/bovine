from .note_builder import NoteBuilder


def test_note_builder_basic():
    result = NoteBuilder("account", "url", "content").build()

    assert result["@context"] == "https://www.w3.org/ns/activitystreams"
    assert result["type"] == "Note"
    assert result["content"] == "content"
