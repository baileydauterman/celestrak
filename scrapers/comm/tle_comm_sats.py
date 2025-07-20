import time
from celestrak import *

while True:
    for sat in CelestrakCommunicationSatellites:
        scraper = CelestrakScraper(
            sat,
            CelestrakFileFormats.TWO_LINE_ELEMENT,
            "/data/comm"
        )
        scraper.get_and_write()

    time.sleep(86400)