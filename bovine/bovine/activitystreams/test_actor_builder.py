from bovine.types import Visibility

from .actor_builder import ActorBuilder


def test_basic_build():
    result = ActorBuilder("name").build()

    assert result["@context"] == "https://www.w3.org/ns/activitystreams"
    assert result["name"] == "name"
    assert result["type"] == "Person"


def test_account_urls():
    result = ActorBuilder("name").with_account_url("account_url").build()

    assert result["id"] == "account_url"
    assert result["inbox"] == "account_url/inbox"
    assert result["outbox"] == "account_url/outbox"


def test_public_key():
    result = (
        ActorBuilder("name")
        .with_account_url("account_url")
        .with_public_key("---key---")
        .build()
    )

    assert isinstance(result["@context"], list)
    assert "https://www.w3.org/ns/activitystreams" in result["@context"]
    assert "https://w3id.org/security/v1" in result["@context"]

    assert result["publicKey"] == {
        "id": "account_url#main-key",
        "owner": "account_url",
        "publicKeyPem": "---key---",
    }


def test_visibility_web():
    result = (
        ActorBuilder("name")
        .with_account_url("account_url")
        .with_public_key("---key---")
        .build(visibility=Visibility.WEB)
    )

    assert isinstance(result["@context"], list)
    assert "https://www.w3.org/ns/activitystreams" in result["@context"]
    assert "https://w3id.org/security/v1" in result["@context"]

    assert "inbox" not in result

    assert result["publicKey"] == {
        "id": "account_url#main-key",
        "owner": "account_url",
        "publicKeyPem": "---key---",
    }
