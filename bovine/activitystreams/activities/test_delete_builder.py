from .delete_builder import DeleteBuilder


def test_delete_builder():
    result = DeleteBuilder("actor", "object_id").build()

    assert result["id"] == "object_id/delete"
    assert result["type"] == "Delete"
    assert "@context" not in result["object"]
