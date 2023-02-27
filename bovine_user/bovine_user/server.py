import logging
from quart import Blueprint, redirect, url_for, current_app, render_template, request
from quart_auth import login_required, Unauthorized, current_user

from .hello_auth import hello_auth
from .utils import create_toml_file

logger = logging.getLogger(__name__)


server = Blueprint("server", __name__, template_folder="../templates/")
server.register_blueprint(hello_auth, url_prefix="/hello")


@server.route("/")
@login_required
async def manage_user():
    hello_sub = current_user.auth_id
    manager = current_app.config["bovine_user_manager"]

    ap_actor, actor = await manager.get_activity_pub(hello_sub)

    if actor:
        return actor.build()

    return await render_template(
        "create.html", register_url=url_for("server.register_user")
    )


@server.route("/toml")
@login_required
async def toml_file():
    hello_sub = current_user.auth_id
    manager = current_app.config["bovine_user_manager"]

    user = await manager.get(hello_sub)

    return (
        create_toml_file(user),
        200,
        {
            "Content-Type": "text/toml",
            "Content-Disposition": f'attachment; filename="{user.handle_name}.toml"',
        },
    )


@server.post("/register")
@login_required
async def register_user():
    await request.get_data(parse_form_data=True)
    handle = (await request.form)["handle"]

    hello_sub = current_user.auth_id
    manager = current_app.config["bovine_user_manager"]
    await manager.register(hello_sub, handle)

    return redirect(url_for("server.manage_user"))


@server.errorhandler(Unauthorized)
async def redirect_to_login(*_: Exception):
    return redirect(url_for("server.hello_auth.hello_login"))
