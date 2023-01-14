from .outbox_builder import OutboxBuilder


def test_outbox_builder():
    result = OutboxBuilder("url").build()

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url",
        "orderedItems": [],
        "totalItems": 0,
        "type": "OrderedCollection",
    }


def test_outbox_builder_with_items():
    result = OutboxBuilder("url").with_count(1).with_items([{"item": "1"}]).build()

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url",
        "orderedItems": [{"item": "1"}],
        "totalItems": 1,
        "type": "OrderedCollection",
    }
