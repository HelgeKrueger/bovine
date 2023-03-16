import json

from . import build_signature
from .crypto import content_digest_sha256, generate_public_private_key
from .http_signature import HttpSignature


def test_http_signature():
    public_key, private_key = generate_public_private_key()

    http_signature = HttpSignature().with_field("name", "value")

    signature_string = http_signature.build_signature("key_id", private_key)

    key_id, algorithm, headers, signature = signature_string.split(",")

    assert key_id == 'keyId="key_id"'
    assert algorithm == 'algorithm="rsa-sha256"'
    assert headers == 'headers="name"'
    assert signature.startswith("signature=")


def test_build_signature():
    public_key, private_key = generate_public_private_key()

    http_signature = build_signature("host", "method", "target")

    signature_string = http_signature.build_signature("key_id", private_key)

    key_id, algorithm, headers, signature = signature_string.split(",")

    assert key_id == 'keyId="key_id"'
    assert algorithm == 'algorithm="rsa-sha256"'
    assert headers == 'headers="(request-target) host"'
    assert signature.startswith("signature=")


def test_build_message():
    http_signature = build_signature(
        "myhost.tld", "get", "/path/to/resource"
    ).with_field("date", "Wed, 15 Mar 2023 17:28:15 GMT")

    message = http_signature.build_message()

    assert (
        message
        == """(request-target): get /path/to/resource
host: myhost.tld
date: Wed, 15 Mar 2023 17:28:15 GMT"""
    )

    signature = http_signature.ed25519_sign(
        "z3u2Yxcowsarethebestcowsarethebestcowsarethebest"
    )

    assert (
        signature
        == "z5ahdHCbP9aJEsDtvG1MEZpxPzuvGKYcdXdKvMq5YL21Z2"
        + "umxjs1SopCY2Ap8vZxVjTEf6dYbGuB7mtgcgUyNdBLe"
    )

    didkey = "did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5"

    http_signature.ed25519_verify(didkey, signature)


def test_build_message_post():
    body = json.dumps({"cows": "good"}).encode("utf-8")

    assert body == b'{"cows": "good"}'

    digest = content_digest_sha256(body)

    assert digest == "sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k="

    http_signature = (
        build_signature("myhost.tld", "post", "/path/to/resource")
        .with_field("date", "Wed, 15 Mar 2023 17:28:15 GMT")
        .with_field("digest", digest)
    )

    message = http_signature.build_message()

    assert (
        message
        == """(request-target): post /path/to/resource
host: myhost.tld
date: Wed, 15 Mar 2023 17:28:15 GMT
digest: sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k="""
    )

    signature = http_signature.ed25519_sign(
        "z3u2Yxcowsarethebestcowsarethebestcowsarethebest"
    )

    assert (
        signature
        == "z4vPkJaoaSVQp5DrMb8EvCajJcerW36rsyWDELTWQ3cYmaonnGf"
        + "b8WHiwH54BShidCcmpoyHjanVRYNrXXXka4jAn"
    )

    didkey = "did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5"

    http_signature.ed25519_verify(didkey, signature)
