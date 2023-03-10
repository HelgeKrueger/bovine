from .processing_item import ProcessingItem


def test_get_object_id():
    def id_for_body(body):
        item = ProcessingItem(body)
        return item.object_id()

    assert id_for_body("{}").startswith("remote://")
    assert id_for_body('{"id": "abc"}') == "abc"

    item = ProcessingItem("{}")

    assert item.object_id() == item.object_id()
