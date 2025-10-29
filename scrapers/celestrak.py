import os
import sys
import time
import requests
import logging
import argparse
from logging import Logger
from enum import Enum
from pathlib import Path
from datetime import datetime

class CelestrakFileFormats(Enum):
    THREE_LINE_ELEMENT = 'tle'
    TWO_LINE_ELEMENT = '2le'
    OMM_XML = 'xml'
    OMM_KVN = 'kvn'
    JSON = 'json'
    JSON_PRETTY = 'json-pretty'
    CSV = 'csv'

    def __str__(self):
        return self.value

class CelestrakSpecialInterestSatellites(Enum):
    LAST_30_DAY_LAUNCHES = ("GROUP", 'last-30-days')
    SPACE_STATIONS = ("GROUP", 'stations')
    BRIGHTEST = ("GROUP", 'visual')
    ACTIVE = ("GROUP", 'active')
    ANALYST_SATELLITES = ("GROUP", 'analyst')
    RUSSIAN_ASAT_TEST_DEBRIS = ("GROUP", 'cosmos-1408-debris')
    CHINESE_ASAT_TEST_DEBRIS = ("GROUP", 'fengyum-1c-debris')
    IRIDIUM_33_DEBRIS = ("GROUP", 'iridium-33-debris')
    COSMOS_2251_DEBRIS = ("GROUP", 'cosmos-2251-debris')

class CelestrakWeatherAndEarthResourcesSatellites(Enum):
    WEATHER = ("GROUP", 'weather')
    NOAA = ("GROUP", 'noaa')
    GOES = ("GROUP", 'goes')
    EARTH_RESOURCES = ("GROUP", 'resources')
    SEARCH_AND_RESCUE = ("GROUP", 'sarsat')
    DISASTER_MONITORING = ("GROUP", 'dmc')
    TRACKING_AND_DATA_RELAY_SATELLITE_SYSTEM = ("GROUP", 'tdrss')
    ARGOS_DATA_COLLECTION_SYSTEM = ("GROUP", 'argos')
    PLANET = ("GROUP", 'planet')
    SPIRE = ("GROUP", 'spire')

class CelestrakCommunicationSatellites(Enum):
    ACTIVE_GEO = ("GROUP", 'geo')
    GEO_PROTECTED_ZONE = ("SPECIAL", 'gpz')
    GEO_PROTECTED_ZONE_PLUS =("SPECIAL", 'gpz-plus')
    INTELSAT = ("GROUP", 'intelsat')
    SES = ("GROUP", 'ses')
    EUTELSAT = ("GROUP", 'eutelsat')
    TELESAT = ("GROUP", 'telesat')
    STARLINK = ("GROUP", 'starlink')
    ONEWEB = ("GROUP", 'oneweb')
    QIANFAN = ("GROUP", 'qianfan')
    HULIANWANG = ("GROUP", 'hulianwang')
    KUIPER = ("GROUP", 'kuiper')
    IRIDIUM_NEXT = ("GROUP", 'iridium-NEXT')
    ORBCOMM = ("GROUP", 'orbcomm')
    GLOBALSTAR = ("GROUP", 'globalstar')
    AMATEUR_RADIO = ("GROUP", 'amateur')
    SATNOGS = ("GROUP", 'satnogs')
    EXPERIMENTAL_COMM = ("GROUP", 'x-comm')
    OTHER_COMM = ("GROUP", 'other-comm')

class CelestrakNavigationSatellites(Enum):
    GNSS = ("GROUP", 'gnss')
    GPS_OPERATIONAL = ("GROUP", 'gps-ops')
    GLONASS_OPERATIONAL = ("GROUP", 'glo-ops')
    GALILEO = ("GROUP", 'galileo')
    BEIDOU = ("GROUP", 'beidou')
    SATELLITE_BASED_AUGMENTATION_SYSTEM = ("GROUP", 'sbas')
    NAVY_NAVIGATION_sATELLITE_SYSTEM = ("GROUP", 'nnss')
    RUSSIAN_LEO_NAVIGATION = ("GROUP", 'musson')

class CelestrakScientificSatellites(Enum):
    SPACE_AND_EARTH_SCIENCES = ("GROUP",'science')
    GEODETIC = ("GROUP", 'geodetic')
    ENGINEERING = ("GROUP", 'engineering')
    EDUCATION = ("GROUP", 'education')

class CelestrakMiscellaneousSatellites(Enum):
    MISCELLANEOUS_MILITARY = ("GROUP", 'military')
    RADAR_CALIBRATION = ("GROUP", 'radar')
    CUBE_SATS = ("GROUP", 'cubesat')
    OTHER_SATELLITES = ("GROUP", 'other')
    

class CelestrakScraper():
    CELESTRAK_ENDPOINT = "https://celestrak.org/NORAD/elements/gp.php"

    def __init__(self, constellation_group_name: Enum, file_format: CelestrakFileFormats, working_directory: str, logger: Logger):
        self.params = {
            constellation_group_name.value[0]: constellation_group_name.value[1],
            "FORMAT": file_format.value
        }
        self.constellation_group_name = constellation_group_name.value[1]
        self.working_directory = working_directory
        self.logger = logger
        self.__build_file_name__()
        self.logger.info("%s", self.params)

    def get(self):
        if self.data_exists:
            return False

        self.response = requests.get(self.CELESTRAK_ENDPOINT, self.params)

        if self.response.status_code != 200:
            self.logger.error("Unable to retrieve data from: %s\nReceived status code: %s", self.params, self.response.status_code)

        return True

    def get_and_write(self):
        hit_endpoint = self.get()
        if hit_endpoint:
            with open(self.full_file_path, 'wb') as out_file:
                out_file.write(self.response.content)
            
        self.data_exists = hit_endpoint

    def __build_file_name__(self):
        self.file_name = f"{datetime.now().date().isoformat()}-{self.constellation_group_name}.{self.params["FORMAT"]}"
        self.full_file_path = os.path.join(self.working_directory, self.file_name)
        Path(self.full_file_path).parent.mkdir(parents=True, exist_ok=True)
        self.data_exists = os.path.exists(self.full_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("celestrak")
    parser.add_argument("-c", "--constellations", choices=["misc", "science", "special-interest", "weather", "nav", "comm"], action="append", required=True)
    parser.add_argument("-o", "--output-format", type=CelestrakFileFormats, choices=list(CelestrakFileFormats))
    opts = parser.parse_args()

    if len(opts.constellations) < 1:
        raise Exception ("arguments should be comma separated\nUsage: celstrak misc|science|special-interest|weather|nav|comm")
    
    logger = logging.getLogger(__file__)
    logger.info("Executing with args: %s", opts)

    while True:
        for a in opts.constellations:
            if a == 'misc':
                sats = CelestrakMiscellaneousSatellites
            elif a == 'science':
                sats = CelestrakScientificSatellites
            elif a == 'special-interest':
                sats = CelestrakSpecialInterestSatellites
            elif a == 'weather':
                sats = CelestrakWeatherAndEarthResourcesSatellites
            elif a == 'nav':
                sats = CelestrakNavigationSatellites
            elif a == 'comm':
                sats = CelestrakCommunicationSatellites
            else:
                continue
            
            for sat in sats:
                scraper = CelestrakScraper(
                    sat,
                    opts.output_format,
                    f"/data/{a}",
                    logger
                )
                scraper.get_and_write()
        
        time.sleep(86400)