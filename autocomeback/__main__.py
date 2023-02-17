import asyncio
import json
from itertools import chain
from pathlib import Path

from loguru import logger

from autocomeback.utils import get_data, get_listings

BASE_DIR = Path(__file__).parent.parent


async def main():
    listings = await get_listings()
    data = list(chain(*[await get_data(listing) for listing in listings]))
    with open(BASE_DIR / "autocomeback" / "source.json", "w+") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info("Done")


if __name__ == "__main__":
    asyncio.run(main())
