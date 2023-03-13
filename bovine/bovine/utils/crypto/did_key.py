from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from multiformats import multibase, multicodec


def generate_keys():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    return private_key, public_key


def serialize_private_key(private_key):
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )

    wrapped = multicodec.wrap("ed25519-priv", private_bytes)

    return multibase.encode(wrapped, "base58btc")


def public_key_to_did_key(public_key):
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    wrapped = multicodec.wrap("ed25519-pub", public_bytes)

    return "did:key:" + multibase.encode(wrapped, "base58btc")


def did_key_to_public_key(did):
    assert did.startswith("did:key:")
    decoded = multibase.decode(did[8:])
    codec, key_bytes = multicodec.unwrap(decoded)
    assert codec.name == "ed25519-pub"

    return ed25519.Ed25519PublicKey.from_public_bytes(key_bytes)
