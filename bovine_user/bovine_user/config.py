import secrets
from urllib.parse import urljoin

import aiohttp
import tomli

from .manager import BovineUserManager


async def configure_bovine_user(app):
    with open("bovine_config.toml", "rb") as fp:
        config_data = tomli.load(fp)

    if "session" not in app.config:
        app.config["session"] = aiohttp.ClientSession()

    app.secret_key = config_data["bovine"]["secret_key"]

    app.config["bovine_user_hello_client_id"] = config_data["bovine_user"][
        "hello_client_id"
    ]

    app.config["host"] = config_data["bovine"]["host"]

    app.config["bovine_user_nonce"] = secrets.token_urlsafe(32)

    endpoints = urljoin(config_data["bovine"]["host"], "endpoints/template")
    app.config["bovine_user_manager"] = BovineUserManager(endpoints)
