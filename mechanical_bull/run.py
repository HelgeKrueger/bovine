import asyncio
import logging

from mechanical_bull import mechanical_bull

log_format = "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    filename=("mechanical_bull.log"),
)

asyncio.run(mechanical_bull("helge.toml"))
