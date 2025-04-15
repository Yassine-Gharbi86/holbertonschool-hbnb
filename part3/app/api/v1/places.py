from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Models for nested related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Model for creating a new place (requires owner_id and amenities)
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenity IDs")
})

# Model for updating a place (owner and amenities not updated)
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload
        place_data['owner_id'] = current_user['id']
        errors = {}
        title = place_data.get('title')
        if not isinstance(title, str) or not title.strip():
            errors['title'] = 'Title must be non empty.'

        description = place_data.get('description')
        if not isinstance(description, str) or not description.strip():
            errors['description'] = 'Description must be non empty.'

        price = place_data.get('price')
        if not isinstance(price, (int, float)):
            errors['price'] = 'Price must be a number.'

        elif price < 0:
            errors['price'] = 'Price cannot be negative.'

        latitude = place_data.get('latitude')
        if not latitude or not isinstance(latitude, (int, float)) or not (-90.0 <= latitude <= 90.0):
            errors['latitude'] = 'Latitude must be a valid number between -90 and 90'

    
        longitude = place_data.get('longitude')
        if not longitude or not isinstance(longitude, (int, float)) or not (-180.0 <= longitude <= 180.0):
            errors['longitude'] = 'Longitude must be a valid number between -180 and 180'

        owner_id = place_data.get('owner_id')
        if not isinstance(owner_id, str):
            errors['owner_id'] = 'Owner ID must be a string.'
        elif not facade.user_exists(owner_id):
            errors['owner_id'] = 'Owner not found.'

        if errors:
            return {'errors': errors}, 400

        new_place = facade.create_place(place_data)
        if not new_place:
            return {'error': 'Failed to create place due to internal error.'}, 500

        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner.id,
            'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in new_place.amenities]
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        
        amenities_data = [{
            'id': amenity.id,
            'name': amenity.name
        } for amenity in place.amenities]

        
        reviews_data = [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id if review.user else None
        } for review in place.reviews]
            
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': amenities_data,
            'reviews': reviews_data
        }, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (only if owned by user)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Ensure that only the owner can update the place
        if str(place.owner.id) != current_user['id'] and not current_user.get('is_admin', False):
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            return {'error': 'Place not found or invalid input data'}, 400

        return {'message': 'Place updated successfully'}, 200
        

@api.route('/<place_id>/amenities/<amenity_id>')
class AddAmenityToPlace(Resource):
    @api.response(200, 'Amenity added to place')
    @api.response(404, 'Place or Amenity not found')
    def post(self, place_id, amenity_id):
        """Add an amenity to a place"""
        place = facade.add_amenity_to_place(place_id, amenity_id)
        if not place:
            return {'error': 'Place or Amenity not found'}, 404

        return {
            'message': 'Amenity added to place successfully',
            'place': {
                'id': place.id,
                'title': place.title,
                'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities]
            }
        }, 200

@api.route('/<place_id>/reviews')
class AddReviewToPlace(Resource):
    @api.expect(api.model('NewReview', {
        'text': fields.String(required=True, description='Review text'),
        'rating': fields.Integer(required=True, min=1, max=5, description='Rating (1-5)'),
        'user_id': fields.String(required=True, description='ID of the user')
    }), validate=True)
    @api.response(201, 'Review created and added to place successfully')
    @api.response(404, 'User or Place not found')
    def post(self, place_id):
        """Create and add a review to a place"""
        review_data = api.payload
        review_data['place_id'] = place_id
        review = facade.create_review(review_data)
        if not review:
            return {'error': 'User or Place not found or invalid input'}, 404

        return {
            'message': 'Review created and added successfully',
            'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id} for review in place.reviews]
        }, 201
