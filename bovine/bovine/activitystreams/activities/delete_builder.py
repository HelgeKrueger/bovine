from bovine.activitystreams.common import as_public, build_context
from bovine.activitystreams.objects import tombstone


class DeleteBuilder:
    def __init__(self, actor, object_id):
        self.actor = actor
        self.object_id = object_id
        self.context_builder = build_context()

    def build(self):
        my_tombstone = tombstone(self.object_id)
        my_tombstone = self.context_builder.absorb(my_tombstone)

        return {
            "@context": self.context_builder.build(),
            "id": self.object_id + "/delete",
            "type": "Delete",
            "actor": self.actor,
            "to": [as_public],
            "cc": [self.actor + "/followers"],
            "object": my_tombstone,
        }
