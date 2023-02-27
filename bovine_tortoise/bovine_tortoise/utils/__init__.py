from urllib.parse import urlparse

from tortoise import Tortoise


async def init(db_url: str = "sqlite://db.sqlite3") -> None:
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["bovine_tortoise.models", "bovine_user.models"]},
    )
    await Tortoise.generate_schemas()

    return None


def determine_local_path_from_activity_id(activity_id):
    local_path = urlparse(activity_id).path
    return local_path
