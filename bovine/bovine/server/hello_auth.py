from urllib.parse import urlencode
import json

from quart import Blueprint, redirect, request, current_app


client_id = "XXX"

hello_auth = Blueprint("hello_auth", __name__)


@hello_auth.get("/login")
async def hello_login():
    host_name = "localhost"
    server_port = 5000

    url_to_open = "https://wallet.hello.coop/authorize?" + urlencode(
        {
            "client_id": client_id,
            "nonce": "xxx",
            "redirect_uri": f"http://{host_name}:{server_port}/id_token",
            "response_mode": "form_post",
            "response_type": "id_token",
            "scope": "openid+email",
        }
    ).replace("%2B", "+")

    return redirect(url_to_open)


@hello_auth.post("/id_token")
async def hello_id_token():
    await request.get_data(parse_form_data=True)

    id_token = (await request.form)["id_token"]

    session = current_app.config["session"]
    validation_result = await session.post(
        "https://wallet.hello.coop/oauth/introspect",
        data={"token": id_token, "client_id": client_id, "nonce": "xxx"},
    )

    validation_parsed = json.loads(await validation_result.text())

    sub = validation_parsed["sub"]

    return sub
