import logging
import traceback

logger = logging.getLogger("pro-list")


class ProcessorList:
    def __init__(self):
        self.processors = []

    def add(self, processor):
        self.processors.append(processor)
        return self

    async def apply(self, item, *arguments):
        working = item
        try:
            for processor in self.processors:
                working = await processor(item, *arguments)
                if not working:
                    return
        except Exception as ex:
            logger.error(">>>>> SOMETHING WENT WRONG IN PROCESSING <<<<<<")
            logger.error(ex)
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            item.dump()
