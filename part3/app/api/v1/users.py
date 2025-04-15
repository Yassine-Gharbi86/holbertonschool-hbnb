from flask_restx import Namespace, Resource, fields
from app.services import facade
from werkzeug.utils import secure_filename
import re
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Updated user model to include is_admin attribute
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(required=False, description='Whether the user is an admin', default=False),
    'password': fields.String(required=True, description='User password')
})

def is_valid_email(email):
    # Regular expression to validate email format
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid email format')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        
        # Validate the email format
        if not is_valid_email(user_data['email']):
            return {'error': 'Invalid email format'}, 400

        # Check if all required fields are non-empty
        if not user_data['first_name'] or not user_data['last_name']:
            return {'error': 'First name and last name cannot be empty'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Create user and log for debugging
        new_user = facade.create_user(user_data)

        # Log the created user details to debug the ID assignment
        print(f"Created User: {new_user.id}, Email: {new_user.email}")

        new_user = facade.create_user(user_data)

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
        }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        } for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        current_user = get_jwt_identity()
        if current_user['id'] != user_id:
            return {'error': 'Unauthorized action'}, 403

        updated_data = api.payload

        # Validate email format
        if not is_valid_email(updated_data['email']):
            return {'error': 'Invalid email format'}, 400

        # Validate non-empty names
        if not updated_data['first_name'] or not updated_data['last_name']:
            return {'error': 'First name and last name cannot be empty'}, 400

        # Check if email is taken by another user
        existing_user = facade.get_user_by_email(updated_data['email'])
        if existing_user and existing_user.id != user_id:
            return {'error': 'Email is already registered by another user'}, 400

        # Attempt to update
        updated_user = facade.update_user(user_id, updated_data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'is_admin': updated_user.is_admin
        }, 200