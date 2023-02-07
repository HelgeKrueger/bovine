import json
import logging


logger = logging.getLogger(__name__)


class ProcessingItem:
    def __init__(self, body, authorization={}):
        self.authorization = authorization
        self.body = body
        self.data = None

    def get_data(self):
        if not self.data:
            self.data = json.loads(self.body)
        return self.data

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
