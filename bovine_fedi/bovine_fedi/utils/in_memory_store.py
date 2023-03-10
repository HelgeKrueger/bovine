from bovine_fedi.types import LocalActor


class InMemoryUserStore:
    def __init__(self):
        self.users = {}

    def add_user(self, local_actor: LocalActor):
        self.users[local_actor.name] = local_actor

    async def get_user(self, username: str) -> LocalActor | None:
        if username in self.users:
            return self.users[username]
        return None


class InMemoryObjectStore:
    async def retrieve(self, retriever, object_id, include=[]):
        pass

    async def store(self, owner, item, as_public=False, visible_to=[]):
        pass
