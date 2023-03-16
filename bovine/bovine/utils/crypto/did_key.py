from textwrap import wrap

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from multiformats import multibase, multicodec


def generate_keys():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    return private_key, public_key


def encode_private_key(private_key):
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )

    wrapped = multicodec.wrap("ed25519-priv", private_bytes)

    return multibase.encode(wrapped, "base58btc")


def encode_public_key(public_key):
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    wrapped = multicodec.wrap("ed25519-pub", public_bytes)
    encoded = multibase.encode(wrapped, "base58btc")

    return encoded


def public_key_to_did_key(public_key):
    return "did:key:" + encode_public_key(public_key)


def private_key_to_secret(private_key):
    return "secret_:" + encode_private_key(private_key)


def public_key_to_hey_key(public_key):
    encoded = encode_public_key(public_key)
    return "hey:key:" + " ".join(wrap(encoded, 4))


def private_key_to_hey_secret(private_key):
    encoded = encode_private_key(private_key)
    return "hey:sec:" + " ".join(wrap(encoded, 4))


def did_key_to_public_key(did):
    assert did.startswith("did:key:")
    decoded = multibase.decode(did[8:])
    codec, key_bytes = multicodec.unwrap(decoded)
    assert codec.name == "ed25519-pub"

    return ed25519.Ed25519PublicKey.from_public_bytes(key_bytes)
