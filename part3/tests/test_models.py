from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user_creation():
    user = User("John", "Doe", "john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("✅ User creation test passed!")

def test_place_creation():
    owner = User("Alice", "Smith", "alice.smith@example.com")
    place = Place("Cozy Apartment", "A nice place to stay", 100, 37.7749, -122.4194, owner)
    review = Review("Great stay!", 5, place, owner)
    place.add_review(review)
    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("✅ Place creation and relationship test passed!")

def test_amenity_creation():
    amenity = Amenity("Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("✅ Amenity creation test passed!")

if __name__ == "__main__":
    test_user_creation()
    test_place_creation()
    test_amenity_creation()