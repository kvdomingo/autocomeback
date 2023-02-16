import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from loguru import logger
from requests import HTTPError

LISTINGS_URL = "https://dbkpop.com/tag/comebacks/"

LISTING_TITLE_PATTERN = re.compile(r"^\w+\s+2\d{3}\b")

TODAY = datetime.now()


def get_listings():
    listings = []
    res = requests.get(LISTINGS_URL)
    if not res.ok:
        raise HTTPError(f"{res.status_code}: {res.text}")
    soup = BeautifulSoup(res.text, "lxml")
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


def get_data(url: str):
    logger.info(f"Retrieving URL {url}...")
    res = requests.get(url)
    if not res.ok:
        raise HTTPError(f"{res.status_code}: {res.text}")
    html = res.text

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
