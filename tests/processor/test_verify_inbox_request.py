import pytest

from bovine.processors import InboxItem
from bovine.processors.verify_inbox import verify_inbox_request


@pytest.mark.asyncio
async def test_verify_inbox_request_fails_if_digest_disagrees():
    headers = {
        "Remote-Addr": "127.0.0.1",
        "Host": "static.104.246.107.91.clients.your-server.de",
        "X-Forwarded-For": "5.9.96.111",
        "X-Forwarded-Proto": "https",
        "Connection": "close",
        "Content-Length": "365",
        "User-Agent": "http.rb/5.1.0 (Mastodon/4.0.2; +https://mas.to/)",
        "Date": "Mon, 16 Jan 2023 13:36:41 GMT",
        "Accept-Encoding": "gzip",
        "Digest": "SHA-256=FcyytKo95bGMpq32o8NvZC3gvj+AsdYU6H6mgm3WEzs=",
        "Content-Type": "application/activity+json",
        "Signature": 'keyId="https://mas.to/users/helgek#main-key",algorithm="rsa-sha256",headers="(request-target) host date digest content-type",signature="h5zVqX9meMfxwd8dBy4AeVVPqCWgLCLJtmQCFBcDtvppWb3dR4koiiCZTHRd+39HmsYGUmPQBQ5LrRznjdQ7ApnBjIPSU2ypGcKXSkgvL7MG3lb0Fx2UFYko8SdBuhZN7MaByBnw4YYRzQvoszS56oQw1prRzoFTywo0xM+Oi8Wwnq5piOqNzxAGCHgmsefTocmbpOXxxWUIESwv/ii42HEuF4WmwbZ9C6sPdbcbSPuaZgwhaOwUKA0pVV1f6oELNtFkxXYiqTl0hqX/x69afaLW5kHqieMGMJmnV9MeY3klRT7G5M0x/YeNUotkgDzlMuok4s8sCH5/WYzrLrvSWw=="',
    }
    body = b"{}"

    item = InboxItem(headers, body)

    assert not await verify_inbox_request(None, item)


@pytest.mark.asyncio
async def test_verify_inbox_request():
    headers = {
        "Remote-Addr": "127.0.0.1",
        "Host": "static.104.246.107.91.clients.your-server.de",
        "X-Forwarded-For": "5.9.96.111",
        "X-Forwarded-Proto": "https",
        "Connection": "close",
        "Content-Length": "365",
        "User-Agent": "http.rb/5.1.0 (Mastodon/4.0.2; +https://mas.to/)",
        "Date": "Mon, 16 Jan 2023 13:36:41 GMT",
        "Accept-Encoding": "gzip",
        "Digest": "SHA-256=FcyytKo95bGMpq32o8NvZC3gvj+AsdYU6H6mgm3WEzs=",
        "Content-Type": "application/activity+json",
        "Signature": 'keyId="https://mas.to/users/helgek#main-key",algorithm="rsa-sha256",headers="(request-target) host date digest content-type",signature="h5zVqX9meMfxwd8dBy4AeVVPqCWgLCLJtmQCFBcDtvppWb3dR4koiiCZTHRd+39HmsYGUmPQBQ5LrRznjdQ7ApnBjIPSU2ypGcKXSkgvL7MG3lb0Fx2UFYko8SdBuhZN7MaByBnw4YYRzQvoszS56oQw1prRzoFTywo0xM+Oi8Wwnq5piOqNzxAGCHgmsefTocmbpOXxxWUIESwv/ii42HEuF4WmwbZ9C6sPdbcbSPuaZgwhaOwUKA0pVV1f6oELNtFkxXYiqTl0hqX/x69afaLW5kHqieMGMJmnV9MeY3klRT7G5M0x/YeNUotkgDzlMuok4s8sCH5/WYzrLrvSWw=="',
    }
    body = b'{"@context":"https://www.w3.org/ns/activitystreams","id":"https://mas.to/users/helgek#follows/4321939/undo","type":"Undo","actor":"https://mas.to/users/helgek","object":{"id":"https://mas.to/ec9bfe97-c26f-4a4d-94d2-fff72d0c489a","type":"Follow","actor":"https://mas.to/users/helgek","object":"https://static.104.246.107.91.clients.your-server.de/activitypub/test"}}'

    item = InboxItem(headers, body)

    assert await verify_inbox_request(None, item)
