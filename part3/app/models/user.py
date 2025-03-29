import re
from .Base_Model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name[:50]
        self.last_name = last_name[:50]
        self.email = email if self.validate_email(email) else None
        self.is_admin = is_admin

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