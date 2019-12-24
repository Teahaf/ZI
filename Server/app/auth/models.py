"""Auth models."""

from datetime import datetime
from app import DB, BCRYPT
from flask_login import UserMixin
from app import LOGIN_MANAGER


class User(UserMixin, DB.Model):
    """User model."""
    __tablename__ = 'users'

    id = DB.Column(DB.Integer, primary_key=True)
    user_name = DB.Column(DB.String(50))
    user_email = DB.Column(DB.String(60), unique=True, index=True)
    user_password = DB.Column(DB.String(80))
    registration_date = DB.Column(DB.DateTime, default=datetime.now)
    role = DB.Column(DB.String(50), default='user')
    max_size = DB.Column(DB.Integer)

    def check_password(self, password):
        """Check entered password."""
        return BCRYPT.check_password_hash(self.user_password, password)

    @classmethod
    def create_user(cls, user, email, password, is_admin=False):
        """Create user."""
        pass_hash = BCRYPT.generate_password_hash(password).decode('utf-8')
        user = cls(user_name=user,
                   user_email=email,
                   user_password=pass_hash,
                   max_size = 15000)
        if is_admin:
            user.role = 'admin'

        DB.session.add(user)
        DB.session.commit()

        return user

    @classmethod
    def create_admin(cls, user, email, password):
        """Create admin."""
        cls.create_user(user, email, password, is_admin=True)

    @LOGIN_MANAGER.user_loader
    def load_user(id):
        """Fetch user object."""
        return User.query.get(int(id))
