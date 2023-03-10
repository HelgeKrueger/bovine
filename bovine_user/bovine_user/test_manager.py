from bovine.activitypub.actor import ActivityPubActor
from bovine.activitystreams.actor_builder import ActorBuilder

from bovine_user.utils.test import db_url  # noqa F401
from examples.basic_app import app

from .manager import BovineUserManager


async def test_bovine_user_manager(db_url):  # noqa F811
    uuid = "uuid"

    manager = BovineUserManager("https://my_domain")

    assert await manager.get(uuid) is None

    user = await manager.register(uuid, "handle")
    assert user.handle_name == "handle"

    assert await manager.get(uuid) == user
    assert await manager.get_user_for_name("handle")


async def test_endpoint(db_url):  # noqa F811
    uuid = "uuid"

    manager = BovineUserManager("https://my_domain")

    user = await manager.register(uuid, "handle")

    first_endpoint = user.endpoints[0].name

    info = await manager.resolve_endpoint(first_endpoint)

    assert info.bovine_user.handle_name == "handle"


async def test_get_acitivity_pub(db_url):  # noqa F811
    async with app.app_context():
        app.config["session"] = "session"
        uuid = "uuid"

        manager = BovineUserManager("https://my_domain")

        await manager.register(uuid, "handle")

        activity_pub_actor, actor = await manager.get_activity_pub(uuid)

        assert isinstance(activity_pub_actor, ActivityPubActor)
        assert isinstance(actor, ActorBuilder)


async def test_bovine_user_manager_user_count(db_url):  # noqa F811
    manager = BovineUserManager("https://my_domain")
    assert await manager.user_count() == 0

    await manager.register("uuid", "handle")
    assert await manager.user_count() == 1
