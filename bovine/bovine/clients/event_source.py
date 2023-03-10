import aiohttp

from bovine.types import ServerSentEvent


class EventSource:
    def __init__(self, session, url, headers={}):
        self.session = session
        self.url = url
        self.headers = headers
        self.response = None

    async def create_response(self):
        timeout = aiohttp.ClientTimeout(total=None)

        self.response = await self.session.get(
            self.url,
            headers={"Accept": "text/event-stream", **self.headers},
            timeout=timeout,
        )

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.response is None:
            await self.create_response()

        to_parse = ""
        async for line_in_bytes in self.response.content:
            line = line_in_bytes.decode("utf-8")
            if line[0] == ":":
                continue
            if line == "\n":
                event = ServerSentEvent.parse_utf8(to_parse)
                return event
            else:
                to_parse = f"{to_parse}{line}"
