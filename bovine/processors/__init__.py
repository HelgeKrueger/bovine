import json


class InboxItem:
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body
        self.data = None

    def get_data(self):
        if not self.data:
            self.data = json.loads(self.body)
        return self.data

    def dump(self):
        print("###########################################################")
        print()
        print("---HEADERS----")
        print(json.dumps(self.headers))
        print()
        print("---BODY----")
        print(self.body.decode("utf-8"))
        print()
        print()
