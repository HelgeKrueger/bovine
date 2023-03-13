from cryptography.hazmat.primitives.asymmetric import ed25519

from .did_key import did_key_to_public_key, generate_keys, public_key_to_did_key

did_example = "did:key:z6MkiTBz1ymuepAQ4HEHYSF1H8quG5GLVVQR3djdX3mDooWp"


def test_encode_private_key():
    _, public_key = generate_keys()
    did = public_key_to_did_key(public_key)

    # See https://w3c-ccg.github.io/did-method-key/#ed25519-x25519
    # These DID always start with z6Mk.

    assert did.startswith("did:key:z6Mk")
    assert len(did) == len(did_example)


def test_did_to_public_key():
    public_key = did_key_to_public_key(did_example)

    assert isinstance(public_key, ed25519.Ed25519PublicKey)


def test_encode_private_key_and_back():
    private_key, public_key = generate_keys()
    did = public_key_to_did_key(public_key)
    transformed = did_key_to_public_key(did)

    message = b"Hello did-core!"

    signature = private_key.sign(message)

    # If verification fails an error is thrown

    public_key.verify(signature, message)
    transformed.verify(signature, message)
