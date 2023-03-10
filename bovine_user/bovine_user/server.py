import logging

from bovine.types import Visibility
from quart import Blueprint, current_app, redirect, render_template, request, url_for
from quart_auth import Unauthorized, current_user, login_required
from quart_cors import route_cors

from .hello_auth import hello_auth
from .utils import create_toml_file

logger = logging.getLogger(__name__)


bovine_user_blueprint = Blueprint("server", __name__, template_folder="../templates/")
bovine_user_blueprint.register_blueprint(hello_auth, url_prefix="/hello")

cors_properties = {
    "allow_origin": ["http://localhost:*"],
    "allow_methods": ["GET", "POST"],
    "allow_headers": ["Authorization", "Content-Type", "Last-Event-Id"],
}


@bovine_user_blueprint.route("/")
@route_cors(**cors_properties)
@login_required
async def manage_user():
    hello_sub = current_user.auth_id
    manager = current_app.config["bovine_user_manager"]

    ap_actor, actor = await manager.get_activity_pub(hello_sub)

    if actor:
        if "json" not in request.headers["accept"]:
            return redirect("/buffalo/")
        return actor.build(visibility=Visibility.OWNER)

    return await render_template(
        "create.html", register_url=url_for("server.register_user")
    )


@bovine_user_blueprint.route("/toml")
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


@bovine_user_blueprint.post("/register")
@login_required
async def register_user():
    await request.get_data(parse_form_data=True)
    handle = (await request.form)["handle"]

    hello_sub = current_user.auth_id
    manager = current_app.config["bovine_user_manager"]
    await manager.register(hello_sub, handle)

    return redirect(url_for("server.manage_user"))


@bovine_user_blueprint.errorhandler(Unauthorized)
async def redirect_to_login(*_: Exception):
    return redirect(url_for("server.hello_auth.hello_login"))
