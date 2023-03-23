def determine_summary(obj):
    for key in ["summary", "name", "content"]:
        if obj.get(key):
            return obj[key][:97]
    return
