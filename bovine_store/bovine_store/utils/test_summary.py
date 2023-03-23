from . import determine_summary


def test_determine_summary():
    assert determine_summary({}) is None
    assert determine_summary({"name": "name"}) == "name"
    assert determine_summary({"content": "content"}) == "content"
    assert determine_summary({"summary": "summary"}) == "summary"
