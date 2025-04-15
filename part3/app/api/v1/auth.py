from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for login input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'JWT token issued successfully')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Generate token with user's ID and admin status
        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })

        return {'access_token': access_token}, 200
    
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.response(200, 'Token valid, access granted')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {
            'message': f'Hello, user {current_user["id"]}',
            'is_admin': current_user["is_admin"]
        }, 200
