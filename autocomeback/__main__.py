import json
from itertools import chain
from pathlib import Path

from loguru import logger

from autocomeback.utils import get_data, get_listings

BASE_DIR = Path(__file__).parent.parent


def main():
    listings = get_listings()
    data = list(chain(*[get_data(listing) for listing in listings]))
    with open(BASE_DIR / "autocomeback" / "source.json", "w+") as f:
        json.dump(data, f, indent=2)
    logger.info("Done")


main()
