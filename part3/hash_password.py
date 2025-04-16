from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Password to hash
password = "admin1234"

# Generate bcrypt hash
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

print("Hashed Password: ", hashed_password)
