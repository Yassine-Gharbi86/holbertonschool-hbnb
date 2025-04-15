import re
from .Base_Model import BaseModel
from app import db, bcrypt
from sqlalchemy.orm import validates

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)




    def __init__(self, first_name, last_name, email, is_admin=False, password=None):
        super().__init__()
        self.first_name = first_name[:50]
        self.last_name = last_name[:50]
        self.email = email if self.validate_email(email) else None
        self.is_admin = is_admin
        self.password = None
        if password:
            self.hash_password(password)

    def validate_email(self, email):
        """Validates email format."""
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, email) is not None
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)