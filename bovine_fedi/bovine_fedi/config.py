import aiohttp
from bovine.utils.signature_checker import SignatureChecker

from .caches import build_public_key_fetcher
from .utils.queue_manager import QueueManager

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": [
                "bovine_fedi.models",
                "bovine_store.models",
                "bovine_user.models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}


async def configure_bovine_fedi(app, bovine_user):
    session = aiohttp.ClientSession()
    public_key_fetcher = build_public_key_fetcher(session, bovine_user)
    signature_checker = SignatureChecker(public_key_fetcher)

    app.config["session"] = session
    app.config["validate_signature"] = signature_checker.validate_signature

    app.config["queue_manager"] = QueueManager()
