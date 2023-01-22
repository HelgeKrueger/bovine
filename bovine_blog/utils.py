import re

from quart import redirect, request


async def rewrite_activity_request():
    accept_header = request.headers.get("accept", "*/*")

    if request.method == "get":
        if any(
            request.path.startswith(url) for url in ["/activitypub", "/testing_notes"]
        ):
            if not re.match(r"application/.*json", accept_header):
                new_path = request.path.replace(r"/activitypub", "")
                new_path = new_path.replace(r"/testing_notes", "")
                print(new_path)
                return redirect(new_path)

    return
