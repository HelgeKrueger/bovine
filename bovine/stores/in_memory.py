from . import LocalUser


class InMemoryUserStore:
    def __init__(self):
        self.users = {}
        self.keys = {}

    def add_user(self, local_user: LocalUser):
        self.users[local_user.name] = local_user

    def get_user(self, username: str) -> LocalUser | None:
        if username in self.users:
            return self.users[username]
        return
