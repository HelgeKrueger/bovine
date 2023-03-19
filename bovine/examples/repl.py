import asyncio
from argparse import ArgumentParser

from ptpython.repl import embed

from bovine import BovineActor

loop = asyncio.get_event_loop()


def config(repl):
    repl.use_code_colorscheme("dracula")
    repl.enable_output_formatting = True


async def repl(config_file):
    async with BovineActor(config_file) as actor:
        activity_factory, object_factory = actor.factories
        inbox = await actor.inbox()
        await embed(
            globals=globals(),
            locals=locals(),
            return_asyncio_coroutine=True,
            patch_stdout=True,
            configure=config,
        )


parser = ArgumentParser()
parser.add_argument("--config_file", default="h.toml")

args = parser.parse_args()

asyncio.run(repl(args.config_file))
