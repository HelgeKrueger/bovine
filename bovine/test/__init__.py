import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def remove_domain_from_url(url):
    assert url.startswith("https://my_domain")

    return url[17:]


def get_user_keys():
    public_key = None
    private_key = None

    if os.path.exists(".files/public_key.pem"):
        with open(".files/public_key.pem") as f:
            public_key = f.read()
    if os.path.exists(".files/private_key.pem"):
        with open(".files/private_key.pem") as f:
            private_key = f.read()

    if public_key and private_key:
        return public_key, private_key

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    if not os.path.exists(".files"):
        os.mkdir(".files")

    with open(".files/public_key.pem", "wb") as f:
        f.write(public_key_pem)

    with open(".files/private_key.pem", "wb") as f:
        f.write(private_key_pem)

    return public_key_pem.decode("utf-8"), private_key_pem.decode("utf-8")
