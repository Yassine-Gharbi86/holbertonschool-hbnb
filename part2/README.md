<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HBnB Project - Business Logic and API Endpoints</title>
</head>
<body>
    <header>
        <div>
            <h1>HBnB Project - Implementation of Business Logic and API Endpoints</h1>
            <p><strong>Authors:</strong> Elyes Bennasri, Yassine Gharbi</p>
        </div>
    </header>
    
    <main>
        <section>
            <h2>Project Overview</h2>
            <p>The <strong>HBnB Project</strong> simulates a <strong>vacation rental platform</strong>, akin to platforms like <strong>Airbnb</strong>. This phase focuses on implementing the business logic and API endpoints that power the application, providing users with the ability to manage and interact with entities like <strong>users</strong>, <strong>places</strong>, <strong>reviews</strong>, and <strong>amenities</strong>.</p>
            <p>The goal of this project was to translate the theoretical design from earlier stages into working code by implementing modular architecture, clean API design, and efficient business logic. Our primary focus was on creating a scalable and maintainable foundation for the application, which involved both business logic and API development.</p>
        </section>

        <section>
            <h2>Objectives and Tasks Achieved</h2>
            <p>In this section, we'll walk you through the steps taken in the project, including our approach to <strong>designing</strong> and <strong>implementing</strong> core features:</p>
            <ul>
                <li><strong>Business Logic Layer Implementation:</strong> We designed the core models such as <strong>User</strong>, <strong>Place</strong>, <strong>Review</strong>, and <strong>Amenity</strong>, ensuring data validation and relationships between entities.</li>
                <li><strong>API Endpoints Development:</strong> Using Flask and Flask-RESTx, we developed RESTful endpoints for each entity, ensuring clear structure and parameter validation.</li>
                <li><strong>Testing and Validation:</strong> We validated business logic and API endpoints through manual testing and automated unit tests, ensuring robust handling of edge cases.</li>
                <li><strong>Integration of the Facade Pattern:</strong> The Facade Pattern simplified communication between the API layer and business logic, making the code easier to maintain.</li>
                <li><strong>Swagger Documentation:</strong> API documentation was automatically generated using Flask-RESTx, providing an interactive reference for developers.</li>
            </ul>
        </section>

        <section>
            <h2>Key Features and Contributions</h2>
            <h3>User Model:</h3>
            <p>We introduced basic validations for <strong>first_name</strong>, <strong>last_name</strong>, and <strong>email</strong>, ensuring that:</p>
            <ul>
                <li>Email follows a valid format.</li>
                <li>First name and last name are non-empty.</li>
            </ul>
            <h3>Place Model:</h3>
            <p>For the <strong>Place</strong> model, we implemented validation to ensure:</p>
            <ul>
                <li>The <strong>title</strong> is non-empty.</li>
                <li>The <strong>price</strong> is a positive number.</li>
                <li><strong>Latitude</strong> is between -90 and 90, and <strong>longitude</strong> is between -180 and 180.</li>
            </ul>
            <h3>Review Model:</h3>
            <p>We ensured that the <strong>text</strong> field is non-empty and validated references to <strong>User</strong> and <strong>Place</strong> entities to ensure data integrity.</p>
        </section>

        <section>
            <h2>Testing and Validation</h2>
            <p>We performed rigorous tests using <strong>cURL</strong> and automated unit tests with Python's <strong>unittest</strong>. This ensured:</p>
            <ul>
                <li>Validation of business logic classes and API responses.</li>
                <li>Correct handling of edge cases like invalid input, missing required fields, and out-of-range values.</li>
                <li>Swagger documentation was consistent with the API implementation.</li>
            </ul>
        </section>

        <section>
            <h2>Swagger Documentation</h2>
            <p>Swagger documentation was generated automatically via Flask-RESTx. This interactive documentation provides an easy way to view the API structure, test endpoints, and understand the expected inputs and outputs.</p>
        </section>

        <footer>
            <p>Created by Yassine Gharbi & Elyes Bennasri. All Rights Reserved.</p>
        </footer>
    </main>
</body>
</html>
