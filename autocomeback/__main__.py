import asyncio
import sys
from itertools import chain
from pathlib import Path

from loguru import logger

from autocomeback.adapters import adapters

BASE_DIR = Path(__file__).parent.parent


async def main(source: str = "DBKPOP"):
    adapter = adapters[source]
    listings = await adapter.get_listings()
    data = list(chain(*[await adapter.get_data(listing) for listing in listings]))
    result = len(await adapter.sync_data(data))
    logger.info(f"{result} Done.")
    return result


if __name__ == "__main__":
    asyncio.run(main((sys.argv[1:2] or ["DBKPOP"])[0]))
