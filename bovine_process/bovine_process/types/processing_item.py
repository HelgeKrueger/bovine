import json
import logging
import uuid

logger = logging.getLogger(__name__)


class ProcessingItem:
    def __init__(self, body, authorization={}):
        self.authorization = authorization
        self.body = body
        self.meta = {}

        self.data = None

        self.object_id()

    def get_data(self):
        if not self.data:
            try:
                self.data = json.loads(self.body)
            except Exception as ex:
                logger.error("Failed to parse with %s", str(ex))
                self.data = {}

        return self.data

    def set_data(self, data):
        self.data = None
        self.body = json.dumps(data)
        self.object_id()
        return self

    def object_id(self):
        data = self.get_data()
        object_id = data.get("id")

        if object_id is None:
            object_id = f"remote://{str(uuid.uuid4())}"
            data["id"] = object_id
            self.data = data
            self.body = json.dumps(data)

        return object_id

    def get_body_id(self) -> str:
        try:
            parsed = json.loads(self.body.decode("utf-8"))
            return parsed["id"]
        except Exception as e:
            logger.info(e)
            return "failed fetching id"

    def dump(self):
        logger.info("###########################################################")
        logger.info("---AUTHORIZATION----")
        logger.info(json.dumps(self.authorization))
        logger.info("---BODY----")
        if isinstance(self.body, str):
            logger.info(self.body)
        else:
            logger.info(self.body.decode("utf-8"))
