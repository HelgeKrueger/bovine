from . import tombstone


def test_tomstone():
    result = tombstone("object_id")
    assert result["type"] == "Tombstone"
    assert result["id"] == "object_id"
