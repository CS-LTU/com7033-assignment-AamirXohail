from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, login_manager


class AppUser(UserMixin, db.Model):
    __tablename__ = "app_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)


@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(int(user_id))
