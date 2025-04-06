from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.models import Place
from app import db


api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})

@api.route('/<place_id>')
class PlaceResource(Resource):
    @jwt_required()
    def put(self, place_id):
        """Update a place"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        place = Place.query.get_or_404(place_id)

       
        if not is_admin and place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        data = request.get_json()
        place.title = data['title']
        place.description = data['description']
        place.price = data['price']
        place.latitude = data['latitude']
        place.longitude = data['longitude']

        db.session.commit()

        return {'message': 'Place updated successfully'}, 200

    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        place = Place.query.get_or_404(place_id)

        
        if not is_admin and place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        db.session.delete(place)
        db.session.commit()

        return {'message': 'Place deleted successfully'}, 200
