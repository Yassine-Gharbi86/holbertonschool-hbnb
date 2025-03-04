<div align="center">
    <h1>
        HBnB Project - Introduction
    </h1>
</div>

<div>
<h2>1. Introduction</h2>
<h3>Purpose of the Document</h3>
<p>This document serves as a comprehensive blueprint for the HBnB project, detailing its architecture, business logic, and API interactions. 
It provides a structured breakdown of the system, ensuring clarity and consistency for developers and stakeholders involved in the project.</p>
<h3>Overview of HBnB Project</h3>
<p> HBnB is a web-based platform for short-term property rentals. The system facilitates property listings, user bookings, and reviews, ensuring 
    a seamless experience for hosts and guests. The document presents the architectural foundation of HBnB, outlining how different components 
    interact to create a scalable and maintainable system.</p>
<h2>2. High-Level Architecture</h2>
 <h3>Overview</h3>
    <p>
        The system follows a layered architecture with a Facade Pattern, ensuring modularity and separation of concerns. Each layer plays a crucial role:
    </p>
    <ul>
        <li><strong>Presentation Layer</strong> – Manages user interactions via the web and API endpoints.</li>
        <li><strong>Business Logic Layer</strong> – Implements application logic, enforcing rules and validations.</li>
        <li><strong>Persistence Layer</strong> – Handles database interactions through ORM (Object-Relational Mapping).</li>
    </ul>
<h3>High-Level Package Diagram</h3>
    <div align="center">
    <img src="Diagrams/H.L.D.jpeg" alt="High-Level Architecture Diagram" style="display: block; padding-bottom: 20px; padding-top: 20px; width: 100%; max-width: 600px; margin-left: auto; margin-right: auto;">
    </div>
</div>
