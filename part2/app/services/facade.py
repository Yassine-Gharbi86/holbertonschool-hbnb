from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------- User Methods ----------
    def create_user(self, user_data):
        """Creates a new user and adds them to the repository."""
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieves a user by their ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieves a user by email (for uniqueness checks)."""
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        """Retrieves all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, updated_data):
        """Update user details"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in updated_data.items():
            setattr(user, key, value)
        self.user_repo.update(user_id, updated_data)
        return user

    # ---------- Amenity Methods ----------
    def create_amenity(self, amenity_data):
        """Creates a new amenity and adds it to the repository."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieves all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an amenity's information."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    # ---------- Place Methods ----------
    def create_place(self, place_data):
        """
        Creates a new place.
        Expects place_data to include: title, description, price, latitude, longitude, owner_id,
        and optionally amenities (a list of amenity IDs).
        Validates that price is non-negative, latitude is between -90 and 90, and longitude between -180 and 180.
        """
        # Validate numeric fields
        try:
            price = float(place_data.get('price', 0))
            latitude = float(place_data.get('latitude', 0))
            longitude = float(place_data.get('longitude', 0))
        except ValueError:
            return None

        if price < 0 or not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            return None

        # Retrieve owner using owner_id
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            return None  # Owner not found

        # Retrieve amenities if provided
        amenities_ids = place_data.get('amenities', [])
        amenities_list = []
        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities_list.append(amenity)

        # Import the Place model here (ensure it's implemented in app/models/place.py)
        from app.models.place import Place
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )
        place.amenities = amenities_list

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a place by its ID (including associated owner and amenities)."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieves all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Updates a place's information.
        Supports updating title, description, price, latitude, and longitude.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Validate and update numeric fields if provided
        if 'price' in place_data:
            try:
                price = float(place_data['price'])
                if price < 0:
                    return None
                place.price = price
            except ValueError:
                return None

        if 'latitude' in place_data:
            try:
                latitude = float(place_data['latitude'])
                if not (-90 <= latitude <= 90):
                    return None
                place.latitude = latitude
            except ValueError:
                return None

        if 'longitude' in place_data:
            try:
                longitude = float(place_data['longitude'])
                if not (-180 <= longitude <= 180):
                    return None
                place.longitude = longitude
            except ValueError:
                return None

        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']

        # For now, owner and amenities are not updated via PUT.
        self.place_repo.update(place_id, place_data)
        return place
        
    def add_amenity_to_place(self, place_id, amenity_id):
        """Retrieve the amenity by its ID from place"""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        if not place or not amenity:
            return None
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            self.place_repo.update(place_id, {"amenities": place.amenities})
            return place
        return place
    
    def add_review_to_place(self, place_id, review_id):
        place = self.get_place(place_id)
        review = self.get_review(review_id)
        if not place or not review:
            return None
        if not hasattr(place, 'reviews'):
            place.reviews = []

    # ---------- Review Methods ----------
    def create_review(self, review_data):
        """
        Creates a new review.
        Expects review_data to include: text, rating, user_id, and place_id.
        Validates that rating is between 1 and 5 and that both user and place exist.
        """
        # Extract user_id and place_id and remove them from review_data
        user_id = review_data.pop("user_id", None)
        place_id = review_data.pop("place_id", None)
        try:
            rating = int(review_data.get("rating"))
        except (ValueError, TypeError):
            return None
        if rating < 1 or rating > 5:
            return None

        user = self.get_user(user_id)
        place = self.get_place(place_id)
        if not user or not place:
            return None

        from app.models.review import Review
        # Create a new review using the user and place objects
        review = Review(user=user, place=place, **review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieves a review by its ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieves all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieves all reviews for a specific place."""
        reviews = []
        for review in self.review_repo.get_all():
            if getattr(review, "place_id", None) == place_id:
                reviews.append(review)
        return reviews

    def update_review(self, review_id, review_data):
        """Updates a review."""
        review = self.get_review(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        """Deletes a review."""
        review = self.get_review(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
