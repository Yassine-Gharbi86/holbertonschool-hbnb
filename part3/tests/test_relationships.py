from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user_place_relationship():
    # Create a user
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")
    db.session.add(user)
    db.session.commit()

    # Create places associated with the user
    place1 = Place(name="Place 1", price=100, owner_id=user.id)
    place2 = Place(name="Place 2", price=200, owner_id=user.id)
    db.session.add(place1)
    db.session.add(place2)
    db.session.commit()

    # Verify the association by retrieving the user and checking their places
    user = User.query.get(user.id)
    assert len(user.places) == 2  # Should have 2 places
    assert place1 in user.places
    assert place2 in user.places


def test_review_relationship():
    # Create reviews for places
    user = User.query.filter_by(email="john.doe@example.com").first()
    place1 = Place.query.first()
    place2 = Place.query.offset(1).first()

    review1 = Review(text="Great place!", rating=5, place_id=place1.id, author_id=user.id)
    review2 = Review(text="Not bad.", rating=3, place_id=place2.id, author_id=user.id)
    db.session.add(review1)
    db.session.add(review2)
    db.session.commit()

    # Verify reviews are correctly linked to places
    place1 = Place.query.get(place1.id)
    place2 = Place.query.get(place2.id)
    
    assert len(place1.reviews) == 1  # Should have 1 review
    assert len(place2.reviews) == 1  # Should have 1 review
    assert review1 in place1.reviews
    assert review2 in place2.reviews


def test_amenity_place_relationship():
    # Create amenities
    amenity1 = Amenity(name="Wi-Fi")
    amenity2 = Amenity(name="Pool")
    db.session.add(amenity1)
    db.session.add(amenity2)
    db.session.commit()

    # Assign amenities to places
    place1 = Place.query.first()
    place2 = Place.query.offset(1).first()

    place1.amenities.append(amenity1)
    place2.amenities.append(amenity2)
    db.session.commit()

    # Verify that amenities are associated with places
    assert amenity1 in place1.amenities
    assert amenity2 in place2.amenities


def test_reverse_amenity_place_relationship():
    # Verify that amenities are linked back to places
    amenity1 = Amenity.query.first()
    amenity2 = Amenity.query.offset(1).first()

    place1 = Place.query.first()
    place2 = Place.query.offset(1).first()

    # Verify reverse relationship (from amenity to place)
    assert place1 in amenity1.places
    assert place2 in amenity2.places


def test_data_integrity():
    # Try inserting a place with a non-existent user (should raise an error)
    invalid_place = Place(name="Invalid Place", price=150, owner_id=9999)  # Assuming 9999 is an invalid user ID
    db.session.add(invalid_place)
    try:
        db.session.commit()
    except Exception as e:
        assert "foreign key" in str(e).lower()  # Should raise a foreign key violation error


# Running all tests
def run_tests():
    test_user_place_relationship()
    test_review_relationship()
    test_amenity_place_relationship()
    test_reverse_amenity_place_relationship()
    test_data_integrity()

    print("All tests passed successfully!")

# Call run_tests function to execute tests
if __name__ == '__main__':
    run_tests()
