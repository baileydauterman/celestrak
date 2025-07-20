import os
import requests
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

class CelestrakSpecialInterestSatellites(Enum):
    LAST_30_DAY_LAUNCHES = 'last-30-days'
    SPACE_STATIONS = 'stations'
    BRIGHTEST = 'visual'
    ACTIVE = 'active'
    ANALYST_SATELLITES = 'analyst'
    RUSSIAN_ASAT_TEST_DEBRIS = 'cosmos-1408-debris'
    CHINESE_ASAT_TEST_DEBRIS = 'fengyum-1c-debris'
    IRIDIUM_33_DEBRIS = 'iridium-33-debris'
    COSMOS_2251_DEBRIS = 'cosmos-2251-debris'

class CelestrakWeatherAndEarthResourcesSatellites(Enum):
    WEATHER = 'weather'
    NOAA = 'noaa'
    GOES = 'goes'
    EARTH_RESOURCES = 'resources'
    SEARCH_AND_RESCUE = 'sarsat'
    DISASTER_MONITORING = 'dmc'
    TRACKING_AND_DATA_RELAY_SATELLITE_SYSTEM = 'tdrss'
    ARGOS_DATA_COLLECTION_SYSTEM = 'argos'
    PLANET = 'planet'
    SPIRE = 'spire'

class CelestrakCommunicationSatellites(Enum):
    ACTIVE_GEO = 'geo'
    # GEO_PROTECTED_ZONE = 'gpz' this is not a `GROUP` it's `SPECIAL`
    # GEO_PROTECTED_ZONE_PLUS = 'gpz-plus' this is not a `GROUP` it's `SPECIAL`
    INTELSAT = 'intelsat'
    SES = 'ses'
    EUTELSAT = 'eutelsat'
    TELESAT = 'telesat'
    STARLINK = 'starlink'
    ONEWEB = 'oneweb'
    QIANFAN = 'qianfan'
    HULIANWANG = 'hulianwang'
    KUIPER = 'kuiper'
    IRIDIUM_NEXT = 'iridium-NEXT'
    ORBCOMM = 'orbcomm'
    GLOBALSTAR = 'globalstar'
    AMATEUR_RADIO = 'amateur'
    SATNOGS = 'satnogs'
    EXPERIMENTAL_COMM = 'x-comm'
    OTHER_COMM = 'other-comm'

class CelestrakNavigationSatellites(Enum):
    GNSS = 'gnss'
    GPS_OPERATIONAL = 'gps-ops'
    GLONASS_OPERATIONAL = 'glo-ops'
    GALILEO = 'galileo'
    BEIDOU = 'beidou'
    SATELLITE_BASED_AUGMENTATION_SYSTEM = 'sbas'
    NAVY_NAVIGATION_sATELLITE_SYSTEM = 'nnss'
    RUSSIAN_LEO_NAVIGATION = 'musson'

class CelestrakScientificSatellites(Enum):
    SPACE_AND_EARTH_SCIENCES = 'science'
    GEODETIC = 'geodetic'
    ENGINEERING = 'engineering'
    EDUCATION = 'education'

class CelestrakMiscellaneousSatellites(Enum):
    MISCELLANEOUS_MILITARY = 'military'
    RADAR_CALIBRATION = 'radar'
    CUBE_SATS = 'cubesats'
    OTHER_SATELLITES = 'other'
    

class CelestrakScraper():
    CELESTRAK_ENDPOINT = "https://celestrak.org/NORAD/elements/gp.php"

    def __init__(self, constellation_group_name: Enum, file_format: CelestrakFileFormats, working_directory: str):
        self.file_format = file_format.value
        self.constellation_group_name = constellation_group_name.value
        self.working_directory = working_directory
        self.__build_file_name__()

    def get(self):
        if self.data_exists:
            return False

        url = self.__build_url__()
        print(url)
        self.response = requests.get(url)

        if self.response.status_code != 200:
            raise Exception(f"Unable to retrieve data from: {url}\nReceived status code: {self.response.status_code}")

        return True

    def get_and_write(self):
        hit_endpoint = self.get()
        if hit_endpoint:
            with open(self.full_file_path, 'wb') as out_file:
                out_file.write(self.response.content)
            
        self.data_exists = hit_endpoint

    def __build_file_name__(self):
        self.file_name = f"{datetime.now().date().isoformat()}-{self.constellation_group_name}.{self.file_format}"
        self.full_file_path = os.path.join(self.working_directory, self.file_name)
        Path(self.full_file_path).parent.mkdir(parents=True, exist_ok=True)
        self.data_exists = os.path.exists(self.full_file_path)

    def __build_url__(self):
        return f"{self.CELESTRAK_ENDPOINT}?GROUP={self.constellation_group_name}&FORMAT={self.file_format}"
