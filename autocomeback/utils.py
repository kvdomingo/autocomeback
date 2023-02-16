import re
from datetime import datetime

from aiohttp import ClientSession
from aiohttp.http_exceptions import HttpProcessingError
from bs4 import BeautifulSoup
from loguru import logger

LISTINGS_URL = "https://dbkpop.com/tag/comebacks/"

LISTING_TITLE_PATTERN = re.compile(r"^\w+\s+2\d{3}\b")

TODAY = datetime.now()


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
