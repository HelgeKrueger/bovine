import asyncio
from argparse import ArgumentParser

from ptpython.repl import embed

from bovine import BovineActor

loop = asyncio.get_event_loop()


async def repl(config_file):
    async with BovineActor(config_file) as actor:
        activity_factory, object_factory = actor.factories
        await embed(
            globals=globals(),
            locals=locals(),
            return_asyncio_coroutine=True,
            patch_stdout=True,
        )


parser = ArgumentParser()
parser.add_argument("--config_file", default="h.toml")

args = parser.parse_args()

asyncio.run(repl(args.config_file))
