from urllib.parse import urlencode
from bovine.activitystreams import (
    build_ordered_collection,
    build_ordered_collection_page,
)


async def ordered_collection_responder(url, count_coroutine, items_coroutine, **kwargs):
    if any(
        kwargs.get(name) is not None for name in ["first", "last", "min_id", "max_id"]
    ):
        return await ordered_collection_page(
            url,
            count_coroutine,
            items_coroutine,
            **kwargs,
        )

    count = await count_coroutine()

    builder = build_ordered_collection(url).with_count(count)

    if count < 10:
        data = await items_coroutine()
        builder = builder.with_items(data["items"])
    else:
        builder = builder.with_first_and_last(f"{url}?first=1", f"{url}?last=1")

    return builder.build(), 200, {"content-type": "application/activity+json"}


async def ordered_collection_page(url, count_coroutine, items_coroutine, **kwargs):
    builder = build_ordered_collection_page(url + "?" + urlencode(kwargs), url)

    data = await items_coroutine(**kwargs)

    if "prev" in data:
        builder = builder.with_prev(f"{url}?{data['prev']}")

    if "next" in data:
        builder = builder.with_next(f"{url}?{data['next']}")

    builder = builder.with_items(data["items"])

    return builder.build(), 200, {"content-type": "application/activity+json"}
