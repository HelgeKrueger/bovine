from bovine.types import InboxItem, LocalUser


def dismiss_delete(callback):
    async def on_delete_perform(
        local_user: LocalUser, item: InboxItem
    ) -> InboxItem | None:
        data = item.get_data()

        if data["type"] == "Delete":
            await callback(local_user, item)
            return

        return item

    return on_delete_perform
