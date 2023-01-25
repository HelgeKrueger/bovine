from .utils import build_create_note_activity_from_data_base_case


def test_build_create_note_activity_from_data_base_case():
    data = {
        "content": "text",
    }
    account_url = "proto://to_account"
    post_url = "proto://to_post"

    result = build_create_note_activity_from_data_base_case(account_url, post_url, data)

    result["published"] = "XXX"
    result["object"]["published"] = "XXX"

    assert result == {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            {
                "inReplyToAtomUri": "ostatus:inReplyToAtomUri",
                "conversation": "ostatus:conversation",
                "ostatus": "http://ostatus.org#",
            },
        ],
        "actor": "proto://to_account",
        "cc": ["proto://to_account/followers"],
        "id": "proto://to_post",
        "object": {
            "@context": "https://www.w3.org/ns/activitystreams",
            "attributedTo": "proto://to_account",
            "cc": ["proto://to_account/followers"],
            "content": "<p>text</p>",
            "id": "proto://to_post",
            "inReplyTo": None,
            "published": "XXX",
            "to": ["https://www.w3.org/ns/activitystreams#Public"],
            "type": "Note",
            "source": {"content": "text", "mediaType": "text/markdown"},
        },
        "published": "XXX",
        "to": ["https://www.w3.org/ns/activitystreams#Public"],
        "type": "Create",
    }


def test_build_create_note_activity_from_data_extra_data():
    data = {
        "content": "text",
        "hashtags": ["#tag1", "#tag2"],
        "conversation": "uid:convo",
        "reply_to_id": "proto://reply_to",
        "reply_to_atom_uri": "proto://reply_atom",
        "reply_to_actor": "proto://reply_actor",
    }
    account_url = "proto://to_account"
    post_url = "proto://to_post"

    result = build_create_note_activity_from_data_base_case(account_url, post_url, data)

    assert "object" in result
    obj = result["object"]

    assert obj["to"] == ["https://www.w3.org/ns/activitystreams#Public"]
    assert set(obj["cc"]) == {"proto://to_account/followers", "proto://reply_actor"}
    assert obj["inReplyTo"] == "proto://reply_to"
    assert obj["inReplyToAtomUri"] == "proto://reply_atom"
    assert obj["conversation"] == "uid:convo"
