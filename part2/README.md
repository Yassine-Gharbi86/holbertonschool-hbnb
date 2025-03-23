# HBnB Project - Implementation of Business Logic and API Endpoints

**Authors:** Elyes Bennasri, Yassine Gharbi

---

## Project Overview

The **HBnB Project** simulates a **vacation rental platform**, similar to **Airbnb**. This phase focuses on implementing the business logic and API endpoints that power the application, providing users with the ability to manage and interact with entities like **users**, **places**, **reviews**, and **amenities**.

The goal of this project was to translate the theoretical design from earlier stages into working code by implementing modular architecture, clean API design, and efficient business logic. Our primary focus was on creating a scalable and maintainable foundation for the application, which involved both business logic and API development.

---

## Objectives and Tasks Achieved

In this section, we'll walk you through the steps taken in the project, including our approach to **designing** and **implementing** core features:

- **Business Logic Layer Implementation:** We designed the core models such as **User**, **Place**, **Review**, and **Amenity**, ensuring data validation and relationships between entities.
- **API Endpoints Development:** Using Flask and Flask-RESTx, we developed RESTful endpoints for each entity, ensuring clear structure and parameter validation.
- **Testing and Validation:** We validated business logic and API endpoints through manual testing and automated unit tests, ensuring robust handling of edge cases.
- **Integration of the Facade Pattern:** The Facade Pattern simplified communication between the API layer and business logic, making the code easier to maintain.
- **Swagger Documentation:** API documentation was automatically generated using Flask-RESTx, providing an interactive reference for developers.

---

## Key Features and Contributions

### User Model:
We introduced basic validations for **first_name**, **last_name**, and **email**, ensuring that:
- Email follows a valid format.
- First name and last name are non-empty.

### Place Model:
For the **Place** model, we implemented validation to ensure:
- The **title** is non-empty.
- The **price** is a positive number.
- **Latitude** is between -90 and 90, and **longitude** is between -180 and 180.

### Review Model:
We ensured that the **text** field is non-empty and validated references to **User** and **Place** entities to ensure data integrity.

---

## Testing and Validation

We employed two main forms of testing to ensure the application's correctness.

### Manual Testing (via cURL)
Each of the API endpoints was tested using cURL commands, simulating different types of requests (valid and invalid data). Below is an example of creating a user:

curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{ "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com" }'

php
Copier
Modifier

We also tested edge cases such as missing or empty fields:

curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{ "first_name": "", "last_name": "", "email": "invalid-email" }'

sql
Copier
Modifier

### Unit Testing (via unittest)
Automated unit tests were developed to check the correctness of each endpoint and the underlying business logic. Below is an example unit test for the user creation endpoint:

import unittest from app import create_app

class TestUserEndpoints(unittest.TestCase):

python
Copier
Modifier
def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client()

def test_create_user(self):
    response = self.client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    })
    self.assertEqual(response.status_code, 201)

def test_create_user_invalid_data(self):
    response = self.client.post('/api/v1/users/', json={
        "first_name": "",
        "last_name": "",
        "email": "invalid-email"
    })
    self.assertEqual(response.status_code, 400)
vbnet
Copier
Modifier

### Edge Cases:
We made sure to test boundary values such as:
- **Latitude** and **Longitude** ranges (ensuring that latitude is between -90 and 90, and longitude is between -180 and 180).
- **Invalid email formats** to check for proper validation.
- **Price validations** to ensure that only positive values are accepted for prices.
- **Missing or empty fields** in user creation requests, testing how the API handles incomplete data.
- We also tested for cases where resources like users or places might not exist when performing operations such as retrieving or deleting data.

---

## Swagger Documentation

As part of our testing and validation, Swagger documentation was auto-generated using Flask-RESTx, which served both as:
- A live API documentation interface.
- A reference for developers to see what data is expected in requests and responses.

To access the Swagger documentation, you can navigate to:

http://127.0.0.1:5000/api/v1/

yaml
Copier
Modifier

This documentation provides detailed information about each endpoint's functionality and structure, making it easier for anyone using the API to understand its capabilities.

---

## Footer

Created by Elyes Bennasri & Yassine Gharbi. All Rights Reserved.