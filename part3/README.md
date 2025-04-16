# HBnB Project: Part 3

## Strengthening the Backend with Authentication and Database Integration

Welcome to Part 3 of the HBnB Project! In this stage, we enhance the backend by incorporating user authentication, authorization mechanisms, and persistent storage via SQLAlchemy. We'll be using SQLite for development and configuring MySQL for production environments.

## Overview of Part 3

In this Part 3, we focus on securing the application, integrating a robust database, and setting up a foundation for a production-ready backend with real-world scalability in mind.

## Key Goals

- **User Authentication & Authorization**: Implement JWT-based user authentication with Flask-JWT-Extended, along with role-based access control (admin vs regular users).
- **Database Integration**: Replace the previous in-memory storage with SQLite for development purposes, while preparing MySQL for use in production.
- **CRUD Operations with Persistence**: Refactor CRUD operations to interact directly with a persistent database, ensuring reliable data storage.
- **Schema Design & Visualization**: Use Mermaid.js to design and visualize the database schema, making sure all relationships between entities are clearly represented.
- **Data Integrity & Validation**: Ensure that all data follows necessary validation rules, and that model constraints are enforced.

## Learning Outcomes

By the end of this phase, you'll:

- Implement a secure JWT-based authentication system for your API.
- Set up role-based access control for different user types (admins and regular users).
- Transition from in-memory storage to a SQLite database for development and a MySQL database for production.
- Map out a relational database schema using SQLAlchemy and visualize it with Mermaid.js.
- Ensure that your backend is secure, scalable, and capable of supporting real-world applications with reliable data storage.

## Project Breakdown

The tasks in this phase have been organized in a way that gradually builds towards a complete backend system with authentication, database integration, and scalable functionality:

1. **Enhance the User Model**: Modify the User model to securely store passwords using bcrypt2, and adjust the registration logic to accommodate this change.
2. **Set Up JWT Authentication**: Implement authentication for the API with JWT tokens, ensuring that protected routes can only be accessed by authenticated users.
3. **Role-based Access Control**: Implement access control to restrict specific actions (e.g., admins managing users, places, etc.).
4. **Switch to SQLite Database**: Transition from using in-memory data storage to an SQLite database for development purposes.
5. **Define Models Using SQLAlchemy**: Map the existing models (User, Place, Review, Amenity) to SQLAlchemy, ensuring that all relationships are properly established.
6. **Prepare for Production with MySQL**: Configure MySQL for use in production environments, with SQLite used for local development.
7. **Visualize the Database**: Create an entity-relationship diagram (ERD) using Mermaid.js to help visualize the database schema and entity relationships.

## Database Design

The following Mermaid.js code represents the schema for the project:

![ER Diagram](https://www.mermaidchart.com/raw/e92b8c3f-3d58-4046-a0df-a70b625cbcd9?theme=light&version=v0.1&format=svg)


## Setting Up the Project

1. **Clone the Repository**  
   To get started, clone the repository:

   ```bash
   git clone https://github.com/Yassine-Gharbi86/holbertonschool-hbnb.git
   cd hbnb-project

2. **Install the Required Dependencies**  
   Use the following command to install all necessary dependencies:

   ```bash
   pip install -r requirements.txt

3. **Run the Application**  
   Start the Flask development server with:

   ```bash
   flask run

## Contributors

This project was developed by:

- Elyes Bennasri
- Yassine Gharbi
