from .like_builder import LikeBuilder


def test_like_builder():
    result = (
        LikeBuilder("account", "obj")
        .add_to("target")
        .add_cc("other")
        .with_content("🐮")
        .build()
    )

    assert result["@context"] == "https://www.w3.org/ns/activitystreams"

    assert result["to"] == ["target"]
    assert result["cc"] == ["other"]

    assert result["type"] == "Like"
