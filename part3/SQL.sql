-- Create User Table
CREATE TABLE User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create Place Table
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Create Review Table
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id)
);

-- Create Amenity Table
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

-- Create Place_Amenity Table (Junction Table)
CREATE TABLE Place_Amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE
);

-- Insert Admin User

INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    uuid_generate_v4(),
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$VT4Qhl3C9T.I6trWNe1l1uhDdIjbXJAtPz2.s8/kRWhJF/A1r3.da',
    TRUE
);

-- Insert Initial Amenities
INSERT INTO Amenity (id, name) VALUES
    (uuid_generate_v4(), 'WiFi'),
    (uuid_generate_v4(), 'Swimming Pool'),
    (uuid_generate_v4(), 'Air Conditioning');