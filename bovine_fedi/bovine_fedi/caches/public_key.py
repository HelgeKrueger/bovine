import logging

from bovine_fedi.models import PublicKey

logger = logging.getLogger(__name__)


class PublicKeyCache:
    def __init__(self, key_fetcher):
        self.key_fetcher = key_fetcher

    async def get_for_url(self, url: str) -> str | None:
        item = await PublicKey.get_or_none(url=url)

        if item:
            return item.public_key

        logger.info(f"Fetching public key for {url}")
        public_key = await self.key_fetcher(url)

        if public_key is None:
            logger.warning(f"Fetching public key for {url} failed")
            return None

        try:
            await PublicKey.create(url=url, public_key=public_key)
        except Exception as ex:
            logger.info(
                f"Tried to create public key for {url} but failed with {str(ex)}"
            )

        return public_key
