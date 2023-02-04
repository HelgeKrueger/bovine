import pytest

from .accept_header import is_activity_request


@pytest.mark.parametrize(
    "header",
    [
        'application/ld+json; profile="https://www.w3.org/ns/activitystreams"',
        "application/activity+json",
        "application/activity+json, application/ld+json",
        "application/activity+json, application/ld+json;"
        + 'profile="https://www.w3.org/ns/activitystreams"',
    ],
)
def test_is_activity_request(header):
    assert is_activity_request(header)


@pytest.mark.parametrize(
    "header",
    [
        "text/html",
    ],
)
def test_is_activity_request_fail(header):
    assert not is_activity_request(header)
