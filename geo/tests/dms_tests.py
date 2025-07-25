from geo.dms import DmsCoordinate, DmsCoordinates, Heading
from geo.geo_converter import dms_to_coordinates

dms_coordinates = DmsCoordinates(
    latitude=DmsCoordinate(37, 15, 3.2400, Heading.North),
    longitude=DmsCoordinate(92, 30, 37.44000, Heading.East)
)

coordinates = dms_to_coordinates(dms_coordinates)

if coordinates.latitude != 37.250900000:
    raise Exception(f"Expected lat dec degs to be equal to {37.250900000}")

if coordinates.longitude != 92.51040000:
    raise Exception(f"Expected lat dec degs to be equal to {37.250900000}")
