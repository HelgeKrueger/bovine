import asyncio
from argparse import ArgumentParser

from bovine import BovineActor


async def send_note(config_file, text):
    async with BovineActor(config_file) as actor:
        note = actor.note(text).add_to("https://mas.to/users/themilkman").build()
        create = actor.activity_factory.create(note).build()

        await actor.send_to_outbox(create)


parser = ArgumentParser()
parser.add_argument("text")
parser.add_argument("--config_file", default="h.toml")

args = parser.parse_args()

asyncio.run(send_note(args.config_file, args.text))
