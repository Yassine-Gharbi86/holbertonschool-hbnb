from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        review = facade.create_review(review_data)
        if not review:
            return {'error': 'Invalid input data or user/place not found or invalid rating'}, 400
        return review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        errors = {}

        try:
            rating = int(review_data.get("rating", 0))
            if rating < 1 or rating > 5:
                errors["rating"] = "Rating must be between 1 and 5."
        except (TypeError, ValueError):
            errors["rating"] = "Rating must be a valid integer."

        text = review_data.get("text", "").strip()
        if not text:
            errors["text"] = "Text cannot be empty."
        
        if errors:
            return {"errors": errors}, 400
        
        updated_fields = {
            "text": text,
            "rating": rating
        }

        review = facade.update_review(review_id, updated_fields)
        if not review:
            return {"error": "Review not found"}, 404
        
        return {
            "message": "Review updated successfully",
            "review": review.to_dict()
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            return {'message': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        # If no reviews exist, still return an empty list provided the place exists
        if not facade.get_place(place_id):
            return {'error': 'Place not found'}, 404
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200
