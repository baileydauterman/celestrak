import math
from enum import Enum
from decimal_degrees import Coordinates

class Heading(Enum):
    North = "N"
    South = "S"
    East = "E"
    West = "W"

    def is_latitude(self):
        return self is Heading.North or self is Heading.South
    
    def is_longitude(self):
        return self is Heading.East or self is Heading.West
    
    def from_string(value: str):
        value = value.lower()

        if value == "n" or value == "north":
            return Heading.North
        elif value == "s" or value == "south":
            return Heading.South
        elif value == "w" or value == "west":
            return Heading.West
        elif value == "e" or value == "east":
            return Heading.East
        else:
            raise Exception(f"Unable to determine heading from value: {value}")


class DmsCoordinate:
    def __init__(self, degrees: int, minutes: int, seconds: float, heading: Heading):
        if heading.is_latitude() and abs(degrees) > 90:
            raise Exception(f"Northing and Southing heading degrees must be between -90 and 90. Current is: {degrees}")
        elif heading.is_longitude() and abs(degrees) > 180:
            raise Exception(f"Easting and Westing heading degrees must be between -180 and 180. Current is: {degrees}")
        
        if not (0 <= minutes <= 60):
            raise Exception(f"Minutes must be between 0 and 60 (inclusive): {minutes}")
        
        if not (0 <= seconds <= 60):
            raise Exception(f"Seconds must be between 0 and 60 (inclusive): {seconds}")
        
        self.degrees = degrees
        self.minutes = minutes
        self.seconds = seconds
        self.heading = heading
        
class DmsCoordinates:
    def __init__(self, lat: DmsCoordinate, lon: DmsCoordinate):
        self.latitude = lat
        self.longitude = lon
