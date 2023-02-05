from . import determine_local_path_from_activity_id


def test_determine_local_path():
    activity_id = "https://domain/something/name/uuid/delete"

    local_path = determine_local_path_from_activity_id(activity_id)

    assert local_path == "/something/name/uuid/delete"
