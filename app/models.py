from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager
from .security_utils import hash_password, verify_password


class AppUser(UserMixin, db.Model):
    """
    Simple user model for authentication within the Hospital Management app.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        """Store a hashed version of the given plain-text password."""
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        """Return True if the password matches the stored hash."""
        return verify_password(password, self.password_hash)


@login_manager.user_loader
def load_user(user_id: str):
    """
    Used by Flask-Login to reload the user object from the user ID stored in the session.
    """
    if not user_id:
        return None
    try:
        return AppUser.query.get(int(user_id))
    except ValueError:
        return None
