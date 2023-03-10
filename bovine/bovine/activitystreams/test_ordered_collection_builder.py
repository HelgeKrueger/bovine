from .ordered_collection_builder import OrderedCollectionBuilder


def test_ordered_collection_builder():
    result = OrderedCollectionBuilder("url").build()

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url",
        "totalItems": 0,
        "type": "OrderedCollection",
    }


def test_ordered_collection_builder_with_items():
    result = (
        OrderedCollectionBuilder("url")
        .with_count(1)
        .with_items([{"item": "1"}])
        .build()
    )

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url",
        "orderedItems": [{"item": "1"}],
        "totalItems": 1,
        "type": "OrderedCollection",
    }


def test_ordered_collection_builder_with_fist_last():
    result = (
        OrderedCollectionBuilder("url")
        .with_count(1)
        .with_first_and_last("first", "last")
        .build()
    )

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url",
        "first": "first",
        "last": "last",
        "totalItems": 1,
        "type": "OrderedCollection",
    }
