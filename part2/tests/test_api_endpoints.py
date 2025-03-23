import unittest
import json
from app import create_app

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the app, test client, and create test data for dependent endpoints."""
        self.app = create_app()
        self.client = self.app.test_client()

        # --- Create a test user ---
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "is_admin": False
        })
        if user_response.status_code == 201:
            self.test_user = json.loads(user_response.data)
            print("🔹 User Creation Response:", self.test_user)
        else:
            users_response = self.client.get('/api/v1/users/')
            users = json.loads(users_response.data) if users_response.status_code == 200 else []
            self.test_user = users[0] if users else None

        if not self.test_user:
            self.skipTest("🚨 Skipping tests: No valid test user available")

        # --- Create a test amenity ---
        amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        if amenity_response.status_code == 201:
            self.test_amenity = json.loads(amenity_response.data)
            print("🔹 Amenity Creation Response:", self.test_amenity)
        else:
            amenities_response = self.client.get('/api/v1/amenities/')
            amenities = json.loads(amenities_response.data) if amenities_response.status_code == 200 else []
            self.test_amenity = amenities[0] if amenities else None

        # --- Create a test place ---
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place for API testing",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.test_user["id"],
            "amenities": [self.test_amenity["id"]] if self.test_amenity else []
        })
        if place_response.status_code == 201:
            self.test_place = json.loads(place_response.data)
            print("🔹 Place Creation Response:", self.test_place)
        else:
            places_response = self.client.get('/api/v1/places/')
            places = json.loads(places_response.data) if places_response.status_code == 200 else []
            self.test_place = places[0] if places else None

    # ----- Users Endpoints Tests -----
    def test_get_user_by_id(self):
        response = self.client.get(f'/api/v1/users/{self.test_user["id"]}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["id"], self.test_user["id"])

    def test_update_user(self):
        response = self.client.put(f'/api/v1/users/{self.test_user["id"]}', json={
            "first_name": "Updated",
            "last_name": "User",
            "email": "testuser@example.com",
            "is_admin": False
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["first_name"], "Updated")

    # ----- Amenities Endpoints Tests -----
    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Gym"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Gym")

    def test_get_amenity_by_id(self):
        response = self.client.get(f'/api/v1/amenities/{self.test_amenity["id"]}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["id"], self.test_amenity["id"])

    def test_update_amenity(self):
        response = self.client.put(f'/api/v1/amenities/{self.test_amenity["id"]}', json={
            "name": "Updated Amenity"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Assuming your API returns updated name in the response:
        self.assertEqual(data["name"], "Updated Amenity")

    # ----- Places Endpoints Tests -----
    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "A nice beach house",
            "price": 200.0,
            "latitude": 36.7783,
            "longitude": -119.4179,
            "owner_id": self.test_user["id"],
            "amenities": [self.test_amenity["id"]] if self.test_amenity else []
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Beach House")

    def test_get_place_by_id(self):
        response = self.client.get(f'/api/v1/places/{self.test_place["id"]}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["id"], self.test_place["id"])

    def test_update_place(self):
        response = self.client.put(f'/api/v1/places/{self.test_place["id"]}', json={
            "title": "Updated Place",
            "description": self.test_place.get("description", "A test place"),
            "price": self.test_place["price"],
            "latitude": self.test_place["latitude"],
            "longitude": self.test_place["longitude"]
        })
        self.assertEqual(response.status_code, 200)
        # Your API returns only a message on update; add further checks if it returns updated details.

    # ----- Reviews Endpoints Tests -----
    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.test_user["id"],
            "place_id": self.test_place["id"]
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)
        self.assertEqual(data.get("text"), "Great place!")

    def test_get_review_by_id(self):
        # First, create a review
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Decent place",
            "rating": 4,
            "user_id": self.test_user["id"],
            "place_id": self.test_place["id"]
        })
        review = json.loads(create_response.data)
        review_id = review["id"]
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["id"], review_id)

    def test_update_review(self):
        # First, create a review
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Initial review",
            "rating": 3,
            "user_id": self.test_user["id"],
            "place_id": self.test_place["id"]
        })
        review = json.loads(create_response.data)
        review_id = review["id"]
        # Then, update the review
        update_response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review",
            "rating": 4,
            "user_id": self.test_user["id"],
            "place_id": self.test_place["id"]
        })
        self.assertEqual(update_response.status_code, 200)
        update_data = json.loads(update_response.data)
        self.assertEqual(update_data.get("message"), "Review updated successfully")

    def test_get_reviews_by_place(self):
        # Route: /api/v1/reviews/places/<place_id>/reviews
        response = self.client.get(f'/api/v1/reviews/places/{self.test_place["id"]}/reviews')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()
