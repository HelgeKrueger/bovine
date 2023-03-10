from quart import Blueprint, current_app

from bovine_fedi.version import __version__

info = Blueprint("info", __name__, url_prefix="/info")


@info.get("/nodeinfo2_0")
async def nodeinfo() -> dict:
    user_count = 0

    if "bovine_user_manager" in current_app.config:
        user_manager = current_app.config["bovine_user_manager"]
        if user_manager:
            user_count = await user_manager.user_count()

    user_stat = {
        "total": user_count,
        "activeMonth": user_count,
        "activeHalfyear": user_count,
    }

    return {
        "metadata": {},
        "openRegistrations": False,
        "protocols": ["activitypub"],
        "services": {"inbound": [], "outbound": []},
        "software": {"name": "bovine", "version": __version__},
        "usage": {"users": user_stat},
        "version": "2.0",
    }
