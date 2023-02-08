from bovine.types import ProcessingItem, LocalActor


def dismiss_delete(callback):
    async def on_delete_perform(
        item: ProcessingItem, local_actor: LocalActor, session
    ) -> ProcessingItem | None:
        data = item.get_data()

        if data["type"] == "Delete":
            await callback(local_actor, item, session)
            return None

        return item

    return on_delete_perform
