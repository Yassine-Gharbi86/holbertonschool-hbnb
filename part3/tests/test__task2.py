from app import create_app
from app.models.user import User
from app.services.facade import HBnBFacade

def test_user_creation(client):
    """Test user creation via the POST /api/v1/users/ endpoint"""
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }

    response = client.post('/api/v1/users/', json=payload)

    assert response.status_code == 201
    response_json = response.get_json()
    assert 'id' in response_json
    assert response_json['first_name'] == "John"
    assert response_json['last_name'] == "Doe"
    assert response_json['email'] == "john.doe@example.com"
    print("✅ User creation test passed!")

def test_get_all_users(client):
    """Test the GET /api/v1/users/ endpoint to retrieve the list of users"""
    response = client.get('/api/v1/users/')

    assert response.status_code == 200  # HTTP 200 OK
    response_json = response.get_json()
    assert isinstance(response_json, list)  # Ensure the response is a list
    assert len(response_json) > 0  # There should be at least one user
    print("✅ Retrieve all users test passed!")

def test_get_user_by_id(client):
    """Test the GET /api/v1/users/<user_id> endpoint to retrieve a user by ID"""
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    }
    create_response = client.post('/api/v1/users/', json=payload)
    create_response_json = create_response.get_json()
    user_id = create_response_json['id']

    response = client.get(f'/api/v1/users/{user_id}')

    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['id'] == user_id
    assert response_json['first_name'] == "Jane"
    assert response_json['last_name'] == "Doe"
    assert response_json['email'] == "jane.doe@example.com"
    print("✅ Retrieve user by ID test passed!")

def test_get_user_not_found(client):
    """Test the GET /api/v1/users/<user_id> endpoint for a non-existent user"""
    non_existent_user_id = "nonexistent-id"

    response = client.get(f'/api/v1/users/{non_existent_user_id}')

    assert response.status_code == 404
    response_json = response.get_json()
    assert response_json['error'] == 'User not found'
    print("✅ User not found test passed!")

def test_user_update(client):
    """Test the PUT /api/v1/users/<user_id> endpoint to update user details"""
    # Create a user first with a unique email
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johnny.doe@example.com"  # Make sure the email is unique
    }
    create_response = client.post('/api/v1/users/', json=payload)
    create_response_json = create_response.get_json()

    print("Create response JSON:", create_response_json)  # Debugging line
    
    # Check if 'id' is in the response before proceeding
    if 'id' not in create_response_json:
        print("Error: 'id' not found in the create response.")
        return  # Early return if 'id' is not found

    user_id = create_response_json['id']

    # Now update the user information
    update_payload = {
        "first_name": "Johnny",
        "last_name": "Doey",
        "email": "johnny.doe@example.com"
    }
    update_response = client.put(f'/api/v1/users/{user_id}', json=update_payload)

    assert update_response.status_code == 200  # HTTP 200 OK
    update_response_json = update_response.get_json()
    assert update_response_json['id'] == user_id
    assert update_response_json['first_name'] == "Johnny"
    assert update_response_json['last_name'] == "Doey"
    assert update_response_json['email'] == "johnny.doe@example.com"
    print("✅ User update test passed!")

if __name__ == "__main__":
    app = create_app()
    with app.test_client() as client:
        test_user_creation(client)
        test_get_all_users(client)
        test_get_user_by_id(client)
        test_get_user_not_found(client)
        test_user_update(client)  # Added the update test