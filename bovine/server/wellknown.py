from quart import Blueprint, current_app, request

from bovine.utils.parsers import parse_account_name

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

    domain = current_app.config["DOMAIN"]

    account_name, account_domain = parse_account_name(resource[5:])

    if account_domain and account_domain != domain:
        return {"status": "not found"}, 404

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
