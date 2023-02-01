from quart import Blueprint, current_app, render_template, send_from_directory

html_blueprint = Blueprint("html_blueprint", __name__, template_folder="./templates/")


@html_blueprint.get("/")
async def index():
    contents = await current_app.config["data_store"].index_contents()

    domain_name = current_app.config["domain_name"]

    contents = sorted(contents, key=lambda x: x["published"], reverse=True)

    return await render_template(
        "index.html", entries=contents, domain_name=domain_name
    )


@html_blueprint.get("/style.css")
async def stylesheet():
    return await send_from_directory("static", "style.css")


@html_blueprint.get("/<username>")
@html_blueprint.get("/<username>/")
async def user(username):
    contents = await current_app.config["data_store"].user_contents(username)
    domain_name = current_app.config["domain_name"]

    contents = sorted(contents, key=lambda x: x["published"], reverse=True)

    return await render_template(
        "user.html", entries=contents, domain_name=domain_name, username=username
    )


@html_blueprint.get("/<username>/<uuid>")
async def post(username, uuid):
    content = await current_app.config["data_store"].user_post(username, uuid)
    if content is None:
        return {"status": "not found"}, 404

    domain_name = current_app.config["domain_name"]

    return await render_template(
        "post.html", entry=content, domain_name=domain_name, username=username
    )
