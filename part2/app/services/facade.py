from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Creates a new user and adds them to the repository."""
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

    def get_place(self, place_id):
        """To be implemented in later tasks."""
        pass