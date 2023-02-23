from bovine_core.activitystreams.common import build_context


class TombstoneBuilder:
    def __init__(self, object_id):
        self.object_id = object_id

    def build(self):
        context = (
            build_context()
            # .add(ostatus="http://ostatus.org#", atomUri="ostatus:atomUri")
            .build()
        )

        return {
            "@context": context,
            "type": "Tombstone",
            "id": self.object_id,
            # "atomUri": self.object_id,
        }
