from quart import Blueprint

info = Blueprint("info", __name__, url_prefix="/info")


@info.get("/nodeinfo2_0")
async def nodeinfo() -> dict:
    return {
        "metadata": {},
        "openRegistrations": False,
        "protocols": ["activitypub"],
        "services": {"inbound": [], "outbound": []},
        "software": {"name": "bovine", "version": "0.0.1"},
        "usage": {"users": {}},
        "version": "2.0",
    }
    # FIXME: Need a way to specify more information here
