from quart import Blueprint, current_app, request

from bovine.utils.parsers import parse_account_name

wellknown = Blueprint("wellknown", __name__, url_prefix="/.well-known")


@wellknown.get("/nodeinfo")
async def nodeinfo() -> tuple[dict, int]:
    domain = current_app.config["DOMAIN"]

    return {
        "links": [
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
                "href": f"https://{domain}/info/nodeinfo2_0",
            }
        ]
    }, 200


@wellknown.get("/webfinger")
async def webfinger() -> tuple[dict, int]:
    resource = request.args.get("resource")

    if not resource or not resource.startswith("acct:"):
        return {"error": "invalid request"}, 400

    domain = current_app.config["DOMAIN"]

    account_name, account_domain = parse_account_name(resource[5:])

    if account_domain and account_domain != domain:
        return {"status": "not found"}, 404

    user_info = await current_app.config["get_user"](account_name)

    if not user_info:
        return {"status": "not found"}, 404

    return (
        {
            "subject": f"acct:{user_info.name}@{domain}",
            "links": [
                {
                    "href": user_info.url,
                    "rel": "self",
                    "type": "application/activity+json",
                }
            ],
        },
        200,
        {"content-type": "application/jrd+json"},
    )


@wellknown.get("/host-meta")
async def wellknown_host_meta():
    host = current_app.config["host"]
    return (
        f"""<?xml version="1.0" encoding="UTF-8"?>
<XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">
  <Link rel="lrdd" template="{host}/.well-known/webfinger?resource={{uri}}"/>
</XRD>""",
        200,
        {"content-type": "application/xrd+xml"},
    )
