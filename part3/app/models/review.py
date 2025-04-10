from .Base_Model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = max(1, min(rating, 5))
        self.place = place
        self.user = user

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id if self.place else None,
            "user_id": self.user.id if self.user else None,
            "created_at": self.created_at.isoformat() if hasattr(self, "created_at") else None,
            "updated_at": self.updated_at.isoformat() if hasattr(self, "updated_at") else None,
        }
