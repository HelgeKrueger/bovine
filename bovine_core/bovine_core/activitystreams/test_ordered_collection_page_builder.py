from .ordered_collection_page_builder import OrderedCollectionPageBuilder


def test_ordered_collection_page_builder():
    result = (
        OrderedCollectionPageBuilder("url?page=1", "url").with_items(["id1"]).build()
    )

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url?page=1",
        "partOf": "url",
        "orderedItems": ["id1"],
        "type": "OrderedCollectionPage",
    }

    result = (
        OrderedCollectionPageBuilder("url?page=1", "url")
        .with_items(["id1"])
        .with_next("next_url")
        .with_prev("prev_url")
        .build()
    )

    assert result == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "url?page=1",
        "next": "next_url",
        "prev": "prev_url",
        "partOf": "url",
        "orderedItems": ["id1"],
        "type": "OrderedCollectionPage",
    }
