from .types import ServerSentEvent


def test_server_sent_event():
    normalized_string = """data: {"json":true}
event: outbox

""".encode(
        "utf-8"
    )

    sse = ServerSentEvent.parse(normalized_string)

    result = sse.encode()

    assert result == normalized_string
