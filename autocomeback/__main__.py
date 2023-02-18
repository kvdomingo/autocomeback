import asyncio
from itertools import chain
from pathlib import Path

from loguru import logger

from autocomeback.utils import get_data, get_listings, sync_data

BASE_DIR = Path(__file__).parent.parent


async def main():
    listings = await get_listings()
    data = list(chain(*[await get_data(listing) for listing in listings]))
    result = len(await sync_data(data))
    logger.info(f"{result} Done.")
    return result


if __name__ == "__main__":
    asyncio.run(main())
