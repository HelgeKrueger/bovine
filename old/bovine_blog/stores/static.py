from collections import defaultdict

from .types import PostEntry


class StaticStore:
    def __init__(self, username="helge"):
        self.username = username
        self.entries = defaultdict(list)

    def add_entry(self, post_entry: PostEntry):
        self.entries[post_entry.author].append(post_entry)

    async def index_contents(self):
        all_entries = sum(self.entries.values(), [])
        return [entry.as_dict() for entry in all_entries]

    async def user_contents(self, username):
        return [entry.as_dict() for entry in self.entries[username]]

    async def user_post(self, username: str, uuid: str):
        for entry in self.entries[username]:
            if entry.local_id == uuid:
                return entry.as_dict()

        return
