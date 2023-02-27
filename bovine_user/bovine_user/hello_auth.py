import json
import logging
from urllib.parse import urlencode, urljoin

from quart import Blueprint, current_app, redirect, request
from quart_auth import AuthUser, login_user

logger = logging.getLogger(__name__)


hello_auth = Blueprint("hello_auth", __name__)


@hello_auth.get("/login")
async def hello_login():
    client_id = current_app.config["bovine_user_hello_client_id"]
    nonce = current_app.config["bovine_user_nonce"]

    redirect_uri = urljoin(current_app.config["host"], request.path)

    url_to_open = "https://wallet.hello.coop/authorize?" + urlencode(
        {
            "client_id": client_id,
            "nonce": nonce,
            "redirect_uri": redirect_uri,
            "response_mode": "form_post",
            "response_type": "id_token",
            "scope": "openid",
        }
    ).replace("%2B", "+")

    return redirect(url_to_open)


@hello_auth.post("/login")
async def hello_id_token():
    await request.get_data(parse_form_data=True)

    id_token = (await request.form)["id_token"]
    client_id = current_app.config["bovine_user_hello_client_id"]
    nonce = current_app.config["bovine_user_nonce"]

    session = current_app.config["session"]
    validation_result = await session.post(
        "https://wallet.hello.coop/oauth/introspect",
        data={"token": id_token, "client_id": client_id, "nonce": nonce},
    )

    validation_parsed = json.loads(await validation_result.text())

    try:
        sub = validation_parsed["sub"]

        logger.info("Signed in with %s", sub)

    except Exception as ex:
        logger.warning(validation_parsed)
        logger.warning(ex)

    login_user(AuthUser(sub))

    return redirect("/")
