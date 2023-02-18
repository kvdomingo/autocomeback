import re
from datetime import datetime
from hashlib import md5
from typing import Any

from aiohttp import ClientSession
from aiohttp.http_exceptions import HttpProcessingError
from bs4 import BeautifulSoup
from loguru import logger
from pytz import timezone

from autocomeback.db import get_firestore_client
from autocomeback.models import Comeback

LISTINGS_URL = "https://dbkpop.com/tag/comebacks/"

LISTING_TITLE_PATTERN = re.compile(r"^\w+\s+2\d{3}\b")

TODAY = datetime.now()

DEFAULT_TZ = timezone("Asia/Seoul")


async def get_listings():
    listings = []
    async with ClientSession() as session:
        async with session.get(LISTINGS_URL) as res:
            if not res.ok:
                raise HttpProcessingError(code=res.status, message=await res.text())
            soup = BeautifulSoup(await res.text(), "lxml")
    titles = soup.find_all(attrs={"class": "entry-title"})
    for title in titles:
        anchor = title.find("a")
        entry_title = anchor.text
        matches = re.match(LISTING_TITLE_PATTERN, entry_title)
        if not matches:
            continue
        extracted_date = matches.group()
        parsed_date = datetime.strptime(extracted_date, "%B %Y")
        if parsed_date.year == TODAY.year and parsed_date.month >= TODAY.month:
            listings.append(anchor.get_attribute_list("href")[0])
    return listings


async def get_data(url: str):
    logger.info(f"Retrieving URL {url}...")
    async with ClientSession() as session:
        async with session.get(url) as res:
            if not res.ok:
                raise HttpProcessingError(code=res.status, message=await res.text())
            html = await res.text()

    logger.info("Processing page source...")
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    thead = table.find("thead")
    head_row = thead.find_all("th")
    headers = [header.text.strip() for header in head_row]

    tbody = table.find("tbody")
    rows = tbody.find_all("tr")
    data = []
    for row in rows:
        cells = row.find_all("td")
        data.append(
            {
                headers[i].lower().replace(" ", "_"): cell.text.strip()
                for i, cell in enumerate(cells)
            }
        )

    logger.info("Extracted data.")
    return data


async def sync_data(data: list[dict[str, Any]]):
    db = get_firestore_client()

    logger.info("Validating data...")
    comebacks = []
    for cb in data:
        dt = (
            datetime.strptime(cb["date"], "%Y-%m-%d")
            .astimezone(DEFAULT_TZ)
            .replace(hour=0 if "japan" in cb["release"].lower() else 18)
        )
        if dt < datetime.now(DEFAULT_TZ):
            continue
        comebacks.append(Comeback(**{**cb, "date": dt}))

    logger.info("Syncing data...")
    coll_ref = db.collection("comebacks")
    docs = [doc async for doc in coll_ref.stream()]
    doc_ids = [doc.id for doc in docs]
    batch = db.batch()
    for comeback in comebacks:
        digest = md5(comeback.json().encode()).hexdigest()
        if digest in doc_ids:
            continue
        doc_ref = coll_ref.document(digest)
        batch.set(doc_ref, comeback.dict())

    logger.info("Purging stale data...")
    for doc in docs:
        comeback = doc.to_dict()
        if comeback["date"].astimezone(DEFAULT_TZ) < datetime.now(DEFAULT_TZ):
            batch.delete(coll_ref.document(doc.id))

    result = await batch.commit()
    return result
