from quart import Blueprint

wellknown = Blueprint("wellknown", __name__, url_prefix="/.well-known")


@wellknown.get("/nodeinfo")
async def nodeinfo() -> dict:
    return {
        "links": [
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
                "href": "FIXME",
            }
        ]
    }
