from .follow_builder import FollowBuilder


def test_follow_builder() -> None:
    data = FollowBuilder("domain", "actor", "tofollow").build()

    assert data["@context"] == "https://www.w3.org/ns/activitystreams"
    assert data["id"].startswith("https://domain/")
    assert data["type"] == "Follow"
    assert data["actor"] == "actor"
    assert data["object"] == "tofollow"
