import asyncio
import os

from argparse import ArgumentParser

from bovine.types import LocalUser
from bovine_tortoise import ManagedDataStore
from bovine.utils.crypto import generate_public_private_key


async def store_user():
    store = ManagedDataStore()
    await store.connect()
    await store.add_user(local_user)
    await store.disconnect()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("--public_key")
    parser.add_argument("--private_key")
    args = parser.parse_args()

    domain = os.environ["DOMAIN"]

    url = f"https://{domain}/activitypub/{args.username}"

    public_key = None
    private_key = None

    if args.public_key or args.private_key:
        with open(args.public_key) as public_key_file:
            with open(args.private_key) as private_key_file:
                private_key = private_key_file.read()
                public_key = public_key_file.read()

    if not public_key or not private_key:
        public_key, private_key = generate_public_private_key()

    if public_key is None or private_key is None:
        print("Failed to generate keys")
        exit(1)

    local_user = LocalUser(
        args.username,
        url,
        public_key,
        private_key,
        "Person",
    )

    asyncio.run(store_user())
