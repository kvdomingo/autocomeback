import asyncio
import json
import sys
from itertools import chain

from loguru import logger

from autocomeback.adapters import adapters


async def main(source: str = "REDDIT"):
    adapter = adapters[source]
    listings = await adapter.get_listings()
    data = list(chain(*[await adapter.get_data(listing) for listing in listings]))
    result = await adapter.sync_data(data)
    logger.info(f"Done.\n{json.dumps(result, indent=2)}")
    return result


if __name__ == "__main__":
    asyncio.run(main((sys.argv[1:2] or ["REDDIT"])[0]))
