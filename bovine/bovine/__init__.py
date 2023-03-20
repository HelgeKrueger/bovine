import aiohttp
import tomli

from .activitypub.actor import ActivityPubActor


class BovineActor(ActivityPubActor):
    def __init__(self, config_file):
        self.config_file = config_file

        with open(config_file, "rb") as fp:
            self.config = tomli.load(fp)

        super().__init__(self.config["account_url"])

    async def init(self, session=None):
        self.session = session
        if session is None:
            self.session = aiohttp.ClientSession()
        self.with_http_signature(
            self.config["public_key_url"],
            self.config["private_key"],
            session=self.session,
        )
        await self.load()

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, *args):
        await self.session.close()
