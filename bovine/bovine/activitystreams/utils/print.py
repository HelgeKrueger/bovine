import bleach


def print_activity(activity):
    if "type" in activity:
        print(f"Type: {activity['type']:10}, Id: {activity.get('id')}")
        print()

    if "object" in activity and isinstance(activity["object"], dict):
        obj = activity["object"]

        print_object(obj)


def print_object(obj):
    if "type" in obj:
        print(f"Type: {obj['type']}")
        print()

    if "name" in obj and obj["name"]:
        print(f"Name: {obj['name']}")
        print()
    if "summary" in obj and obj["summary"]:
        print("Summary")
        print(bleach.clean(obj["summary"], tags=[], strip=True))
        print()

    if "content" in obj and obj["content"]:
        print("Content")
        print(bleach.clean(obj["content"], tags=[], strip=True))
        print()
