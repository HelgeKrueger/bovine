from bovine.utils.test import get_user_keys

from . import (
    content_digest_sha256,
    generate_public_private_key,
    sign_message,
    verify_signature,
)


def test_crypto_sign_verify():
    message = "secret"

    public_key, private_key = get_user_keys()

    signature = sign_message(private_key, message)

    assert verify_signature(public_key, message, signature)


def test_crypto_sign_verify_failure():
    message = "secret"

    public_key, private_key = get_user_keys()

    assert not verify_signature(public_key, message, "")


def test_content_digest_sha256():
    digest = content_digest_sha256("content")

    assert digest.startswith("sha-256=")


def test_generate_public_private_key():
    public_key, private_key = generate_public_private_key()

    assert public_key.startswith("-----BEGIN PUBLIC KEY-----")
    assert public_key.endswith("-----END PUBLIC KEY-----\n")

    assert private_key.startswith("-----BEGIN PRIVATE KEY-----")
    assert private_key.endswith("-----END PRIVATE KEY-----\n")
