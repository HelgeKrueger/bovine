import json

import tomli

import bovine_core.clients.signed_http


class ActivityPubClient:
    def __init__(self, session, public_key_url, private_key, account_url=None):
        self.session = session
        self.public_key_url = public_key_url
        self.private_key = private_key
        self.account_url = account_url

    def set_session(self, session):
        self.session = session

        return self

    async def get(self, url, headers={}):
        return await bovine_core.clients.signed_http.signed_get(
            self.session, self.public_key_url, self.private_key, url, headers
        )

    async def post(self, url, body, headers={}):
        return await bovine_core.clients.signed_http.signed_post(
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

    def server_sent_events(self):
        return bovine_core.clients.signed_http.event_source(
            self.session,
            self.public_key_url,
            self.private_key,
            self.account_url + "/serverSentEvents",
        )

    @staticmethod
    def from_toml_file(file_handle):
        data = tomli.load(file_handle)

        return ActivityPubClient(
            None,
            data["public_key_url"],
            data["private_key"],
            account_url=data["account_url"],
        )
