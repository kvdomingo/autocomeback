import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from loguru import logger
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located,
)
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).parent.parent

CACHED_DATA = BASE_DIR / "autocomeback" / "source.json"


def main(url: str):
    options = Options()
    options.add_argument("-headless")
    with Firefox(options=options) as driver:
        logger.info(f"Retrieving URL {url}...")
        driver.get(url)
        WebDriverWait(driver, 10).until(
            presence_of_all_elements_located((By.CLASS_NAME, "wpDataTable"))
        )
        logger.info("Scraping page source...")
        html = driver.page_source

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

    if CACHED_DATA.exists():
        with open(CACHED_DATA, "r") as f:
            cached = json.load(f)
        data = [*cached, *data]
    with open(CACHED_DATA, "w+") as f:
        json.dump(data, f, indent=2)
    logger.info("Done.")


main(sys.argv[1])
