from .accept_builder import AcceptBuilder


def test_accept_builder():
    result = AcceptBuilder("account", {"an": "object"}).build()

    assert result["@context"] == "https://www.w3.org/ns/activitystreams"
    assert result["id"] == "account#accepts/follows/"
    assert result["type"] == "Accept"
    assert result["actor"] == "account"
    assert result["object"]["an"] == "object"
