from bovine_tortoise.models import StoredObject


class Storage:
    def __init__(self):
        pass

    async def add_object(self, name, data):
        result = await StoredObject.create(name=name, data=data)

        if result.data != data:
            return False

        return True

    async def get_object(self, name):
        return await StoredObject.get_or_none(name=name)
