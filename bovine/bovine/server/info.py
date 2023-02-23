from quart import Blueprint

from bovine import __version__

info = Blueprint("info", __name__, url_prefix="/info")


@info.get("/nodeinfo2_0")
async def nodeinfo() -> dict:
    return {
        "metadata": {},
        "openRegistrations": False,
        "protocols": ["activitypub"],
        "services": {"inbound": [], "outbound": []},
        "software": {"name": "bovine", "version": __version__},
        "usage": {"users": {}},
        "version": "2.0",
    }
    # FIXME: Need a way to specify more information here
