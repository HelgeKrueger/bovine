import json

from .signed_http import signed_get, signed_post


class ActivityPubClient:
    def __init__(self, session, public_key_url, private_key):
        self.session = session
        self.public_key_url = public_key_url
        self.private_key = private_key

    async def get(self, url, headers={}):
        return await signed_get(
            self.session, self.public_key_url, self.private_key, url, headers
        )

    async def post(self, url, body, headers={}):
        return await signed_post(
            self.session, self.public_key_url, self.private_key, url, body, headers
        )

    async def get_ordered_collection(self, url, max_items=None):
        result = await self.get(url)
        result.raise_for_status()

        data = json.loads(await result.text())

        total_number_of_items = data["totalItems"]
        items = []

        if "orderedItems" in data:
            items = data["orderedItems"]

        if len(items) == total_number_of_items:
            return {"total_items": total_number_of_items, "items": items}

        if "first" in data:
            page_response = await self.get(data["first"])
            page_response.raise_for_status()
            page_data = json.loads(await page_response.text())

            items = page_data["orderedItems"]

            while "next" in page_data and len(page_data["orderedItems"]) > 0:
                if max_items and len(items) > max_items:
                    return {"total_items": total_number_of_items, "items": items}

                page_response = await self.get(page_data["next"])
                page_response.raise_for_status()
                page_data = json.loads(await page_response.text())

                items += page_data["orderedItems"]

        return {"total_items": total_number_of_items, "items": items}
