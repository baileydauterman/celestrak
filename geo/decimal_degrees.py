class Coordinates:
    def __init__(self, latitude: float, longitude: float):
        if not (-90 <= latitude <= 90):
            raise Exception(f"Latitude must be between -90 and 90: {latitude}")
        
        if not (-180 <= longitude <= 180):
            raise Exception(f"Longitude must be between -180 and 180: {longitude}")
        
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"
