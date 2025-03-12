from .Base_Model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = max(1, min(rating, 5))
        self.place = place
        self.user = user