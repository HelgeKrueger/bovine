from .context_builder import ContextBuilder


def test_basic_context():
    builder = ContextBuilder()
    result = builder.build()

    assert result == "https://www.w3.org/ns/activitystreams"


def test_with_extensions():
    builder = ContextBuilder().add(
        ostatus="http://ostatus.org#", atomUri="ostatus:atomUri"
    )
    result = builder.build()

    assert result == [
        "https://www.w3.org/ns/activitystreams",
        {"ostatus": "http://ostatus.org#", "atomUri": "ostatus:atomUri"},
    ]


def test_with_additional_list_item():
    builder = ContextBuilder().add("https://w3id.org/security/v1")

    result = builder.build()

    assert result == [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1",
    ]


def test_absorb():
    obj = {
        "@context": ContextBuilder()
        .add(
            "https://w3id.org/security/v1",
            ostatus="http://ostatus.org#",
            atomUri="ostatus:atomUri",
        )
        .build(),
        "prop": "value",
    }

    builder = ContextBuilder()
    obj = builder.absorb(obj)

    assert "@context" not in obj

    result = builder.build()

    assert result == [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1",
        {"ostatus": "http://ostatus.org#", "atomUri": "ostatus:atomUri"},
    ]
