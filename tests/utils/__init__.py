import json

from bovine.types import ProcessingItem


def build_inbox_item_from_json(json_file_name):
    with open(json_file_name, "r") as f:
        return ProcessingItem(f.read())


def get_activity_from_json(json_file_name):
    with open(json_file_name, "r") as f:
        return json.load(f)


fake_post_headers = {
    "Content-Type": "application/activity+json",
    "Signature": "signature",
    "date": "date",
    "host": "host",
    "digest": "XXXxx",
}

fake_get_headers = {
    "Accept": "application/activity+json",
    "date": "date",
    "host": "host",
}
