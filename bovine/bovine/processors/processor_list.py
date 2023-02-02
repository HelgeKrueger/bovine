import logging
import traceback

logger = logging.getLogger("pro-list")

from . import build_do_for_types


class ProcessorList:
    def __init__(self, on_object=False):
        self.processors = []
        self.on_object = on_object

    def add(self, processor):
        self.processors.append(processor)
        return self

    def add_for_types(self, **kwargs):
        return self.add(build_do_for_types(kwargs))

    async def apply(self, item, *arguments):
        if self.on_object:
            if isinstance(item, dict):
                working = item["object"]
            else:
                working = item.get_data()["object"]
        else:
            working = item

        try:
            for processor in self.processors:
                working = await processor(working, *arguments)
                if not working:
                    return

            if self.on_object:
                return item
            else:
                return working
        except Exception as ex:
            logger.error(">>>>> SOMETHING WENT WRONG IN PROCESSING <<<<<<")
            logger.error(ex)
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            item.dump()
