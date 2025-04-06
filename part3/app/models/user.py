import re
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.models import User
from app import db


api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name')
})

@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Modify user information"""
        current_user = get_jwt_identity()

        if current_user['id'] != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.get_json()

        
        if 'email' in data or 'password' in data:
            return {'error': 'You cannot modify email or password'}, 400

        user = User.query.get_or_404(user_id)
        user.first_name = data['first_name']
        user.last_name = data['last_name']

        db.session.commit()

        return {'message': 'User details updated successfully'}, 200
