from bovine.types import InboxItem, LocalUser


def dismiss_delete(callback):
    async def on_delete_perform(
        item: InboxItem, local_user: LocalUser, session
    ) -> InboxItem | None:
        data = item.get_data()

        if data["type"] == "Delete":
            await callback(local_user, item, session)
            return None

        return item

    return on_delete_perform