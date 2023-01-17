from quart import Blueprint, current_app, request

wellknown = Blueprint("wellknown", __name__, url_prefix="/.well-known")


@wellknown.get("/nodeinfo")
async def nodeinfo() -> dict:
    domain = current_app.config["DOMAIN"]

    return {
        "links": [
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
                "href": f"https://{domain}/info/nodeinfo2_0",
            }
        ]
    }


@wellknown.get("/webfinger")
async def webfinger() -> dict:
    resource = request.args.get("resource")

    if not resource or not resource.startswith("acct:"):
        return {"error": "invalid request"}, 400

    account_name = resource[5:]
    domain = current_app.config["DOMAIN"]

    if account_name[0] == "@":
        account_name = account_name[1:]
    if "@" in account_name:
        account_name = account_name.split("@")[0]

    user_info = await current_app.config.data_store.get_user(account_name)

    if not user_info:
        return {"status": "not found"}, 404

    activitypub_profile_url = f"https://{domain}/activitypub/{user_info.name}"

    return {
        "subject": f"acct:{user_info.name}@{domain}",
        "links": [
            {
                "href": activitypub_profile_url,
                "rel": "self",
                "type": "application/activity+json",
            }
        ],
    }
