from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.models import Review, Place
from app import db


api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    def post(self):
        """Create a new review"""
        current_user = get_jwt_identity()
        data = request.get_json()

        place = Place.query.get_or_404(data['place_id'])

        
        if place.owner_id == current_user['id']:
            return {'error': 'You cannot review your own place'}, 400

        
        existing_review = Review.query.filter_by(place_id=place.id, user_id=current_user['id']).first()
        if existing_review:
            return {'error': 'You have already reviewed this place'}, 400

        review = Review(
            text=data['text'],
            rating=data['rating'],
            place=place,
            user=current_user['id']
        )

        db.session.add(review)
        db.session.commit()

        return {'message': 'Review created successfully'}, 201


@api.route('/<review_id>')
class ReviewResource(Resource):
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user = get_jwt_identity()
        review = Review.query.get_or_404(review_id)

        if review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        data = request.get_json()
        review.text = data['text']
        review.rating = data['rating']

        db.session.commit()

        return {'message': 'Review updated successfully'}, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = Review.query.get_or_404(review_id)

        if review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        db.session.delete(review)
        db.session.commit()

        return {'message': 'Review deleted successfully'}, 200
