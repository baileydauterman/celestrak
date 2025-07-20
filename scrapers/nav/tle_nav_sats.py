import time
from celestrak import *

while True:
    for sat in CelestrakNavigationSatellites:
        scraper = CelestrakScraper(
            sat,
            CelestrakFileFormats.TWO_LINE_ELEMENT,
            "/data/nav"
        )
        scraper.get_and_write()

    # wait one day to pull next group of information
    time.sleep(86400)