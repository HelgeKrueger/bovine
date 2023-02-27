import secrets
from urllib.parse import urljoin

from bovine_core.activitypub.actor import ActivityPubActor
from bovine_core.activitystreams import build_actor
from bovine_core.utils.crypto import generate_public_private_key
from quart import current_app

from .models import BovineUser, BovineUserEndpoint, BovineUserKeyPair
from .types import EndpointType


class BovineUserManager:
    def __init__(self, endpoint_path):
        self.endpoint_path = endpoint_path

    async def get(self, hello_sub):
        user = await BovineUser.get_or_none(hello_sub=hello_sub).prefetch_related(
            "endpoints", "keypairs"
        )

        return user

    async def get_activity_pub(self, hello_sub):
        user = await self.get(hello_sub)

        if user is None:
            return None, None

        mapped_endpoints = {x.endpoint_type: x for x in user.endpoints}

        account_url = mapped_endpoints[EndpointType.ACTOR].name

        keypair = user.keypairs[0]
        public_key_url = f"{account_url}#{keypair.name}"

        activity_pub_actor = ActivityPubActor(account_url).with_http_signature(
            public_key_url, keypair.private_key, session=current_app.config["session"]
        )

        actor = (
            build_actor(user.handle_name)
            .with_account_url(account_url)
            .with_inbox(mapped_endpoints[EndpointType.INBOX].name)
            .with_outbox(mapped_endpoints[EndpointType.OUTBOX].name)
            .with_event_source(mapped_endpoints[EndpointType.EVENT_SOURCE].name)
            .with_public_key(keypair.public_key, key_name=keypair.name)
        )

        return activity_pub_actor, actor

    async def get_user_for_name(self, handle_name):
        user = await BovineUser.get_or_none(handle_name=handle_name).prefetch_related(
            "endpoints", "keypairs"
        )
        return user

    async def register(self, hello_sub, handle_name):
        user, _ = await BovineUser.get_or_create(
            hello_sub=hello_sub, defaults={"handle_name": handle_name}
        )

        await self.add_key_pair(user, "serverKey")

        for endpoint_type in EndpointType:
            if endpoint_type != EndpointType.COLLECTION:
                await self._add_endpoint(user, endpoint_type)

        return await self.get(hello_sub)

    async def add_key_pair(self, user: BovineUser, name: str):
        public_key, private_key = generate_public_private_key()
        await BovineUserKeyPair.create(
            bovine_user=user, name=name, public_key=public_key, private_key=private_key
        )

    async def _add_endpoint(self, user: BovineUser, endpoint_type: EndpointType):
        await BovineUserEndpoint.create(
            bovine_user=user,
            endpoint_type=endpoint_type,
            name=self._build_endpoint_name(),
            stream_name=endpoint_type.value,
        )

    def _build_endpoint_name(self):
        random_part = secrets.token_urlsafe(32)
        return urljoin(self.endpoint_path, random_part)

    async def resolve_endpoint(self, endpoint):
        user_endpoint = await BovineUserEndpoint.get_or_none(
            name=endpoint
        ).prefetch_related("bovine_user")

        return user_endpoint
