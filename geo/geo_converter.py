import math
from dms import DmsCoordinate, DmsCoordinates
from decimal_degrees import Coordinates

def dms_to_decimal(dms: DmsCoordinate):
    return math.copysign(abs(dms.degrees) + dms.minutes / 60 + dms.seconds / 3600, dms.degrees)

def decimal_to_dms(degree: float):
    pass

def dms_to_coordinates(dms_coordinates: DmsCoordinates):
    return Coordinates(
        dms_to_decimal(dms_coordinates.latitude),
        dms_to_decimal(dms_coordinates.longitude)
    )
