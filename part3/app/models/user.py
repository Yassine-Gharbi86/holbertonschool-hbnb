import re
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.models import User
from app import db

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=False, description='User email'),
    'password': fields.String(required=False, description='User password')
})

@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Modify user information"""
        current_user = get_jwt_identity()

        
        if current_user['id'] != user_id and not current_user['is_admin']:
            return {'error': 'Unauthorized action'}, 403

        data = request.get_json()

        
        if 'email' in data or 'password' in data:
            if not current_user['is_admin']:
                return {'error': 'You cannot modify email or password'}, 400

        
        user = User.query.get_or_404(user_id)
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data and current_user['is_admin']:
            user.email = data['email']
        if 'password' in data and current_user['is_admin']:
            user.hash_password(data['password'])

        db.session.commit()

        return {'message': 'User details updated successfully'}, 200

@api.route('/')
class UserCreate(Resource):
    @jwt_required()
    @api.expect(user_model)
    def post(self):
        """Create a new user (admin only)"""
        current_user = get_jwt_identity()

        
        if not current_user['is_admin']:
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()

        
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {'error': 'Email already registered'}, 400

        
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        new_user.hash_password(data['password'])
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201
