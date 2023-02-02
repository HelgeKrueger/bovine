import logging
import traceback

logger = logging.getLogger("bov-proc")


async def do_nothing(item, *args):
    return item


activity_streams_activities = [
    "Accept",
    "Add",
    "Announce",
    "Arrive",
    "Block",
    "Create",
    "Delete",
    "Dislike",
    "Follow",
    "Flag",
    "Ignore",
    "Invite",
    "Join",
    "Leave",
    "Like",
    "Listen",
    "Move",
    "Offer",
    "Read",
    "Reject",
    "Remove",
    "TentativeAccept",
    "TentativeReject",
    "Travel",
    "Undo",
    "Update",
    "View",
]

activity_streams_objects = [
    "Activity",
    "Application",
    "Article",
    "Audio",
    "Collection",
    "CollectionPage",
    "Relationship",
    "Document",
    "Event",
    "Group",
    "Image",
    "IntransitiveActivity",
    "Note",
    "Object",
    "OrderedCollection",
    "OrderedCollectionPage",
    "Organization",
    "Page",
    "Person",
    "Place",
    "Profile",
    "Question",
    "Service",
    "Tombstone",
    "Video",
]

activity_streams_activities_or_objects = (
    activity_streams_activities + activity_streams_objects
)

do_nothing_for_all_activities_or_objects = {
    activity: do_nothing for activity in activity_streams_activities_or_objects
}


class ByActivityType:
    def __init__(self, actions: dict):
        self.actions = actions

    async def act(self, item, *args):
        try:
            if isinstance(item, dict):
                item_type = item["type"]
            else:
                item_type = item.get_data()["type"]

            return await self.actions[item_type](item, *args)
        except Exception as ex:
            logger.error(f"Something went wrong with {ex} during procession")
            for log_line in traceback.format_exc().splitlines():
                logger.error(log_line)
