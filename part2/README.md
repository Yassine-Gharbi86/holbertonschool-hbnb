# HBnB Project - Implementation of Business Logic and API Endpoints

**Authors:** Elyes Bennasri, Yassine Gharbi

---

## Project Overview

The **HBnB Project** simulates a **vacation rental platform**, akin to platforms like **Airbnb**. This phase focuses on implementing the business logic and API endpoints that power the application, providing users with the ability to manage and interact with entities like **users**, **places**, **reviews**, and **amenities**.

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

We performed rigorous tests using **cURL** and automated unit tests with Python's **unittest**. This ensured:

- Validation of business logic classes and API responses.
- Correct handling of edge cases like invalid input, missing required fields, and out-of-range values.
- Swagger documentation was consistent with the API implementation.

---

## Swagger Documentation

Swagger documentation was generated automatically via Flask-RESTx. This interactive documentation provides an easy way to view the API structure, test endpoints, and understand the expected inputs and outputs.

---

## Footer

Created by Yassine Gharbi & Elyes Bennasri . All Rights Reserved.
