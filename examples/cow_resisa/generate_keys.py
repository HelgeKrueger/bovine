import os

from bovine.utils.crypto import generate_public_private_key

if os.path.exists("public_key.pem") or os.path.exists("private_key.pem"):
    print("Public or Private key file already exists.")
    exit(1)

public_key, private_key = generate_public_private_key()

with open("public_key.pem", "w") as f:
    f.write(public_key)
with open("private_key.pem", "w") as f:
    f.write(private_key)
