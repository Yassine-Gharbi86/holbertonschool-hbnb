from .Base_Model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title[:100]
        self.description = description
        self.price = max(price, 0)  # Ensuring a positive value
        self.latitude = min(max(latitude, -90.0), 90.0)  # Bound between -90 and 90
        self.longitude = min(max(longitude, -180.0), 180.0)  # Bound between -180 and 180
        self.owner = owner  # Should be an instance of User
        self.reviews = []  
        self.amenities = []

    def add_review(self, review):
        """Adds a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Adds an amenity to the place."""
        self.amenities.append(amenity)