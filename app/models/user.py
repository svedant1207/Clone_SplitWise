from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    
    # Login identity
    email = db.Column(db.String(120), nullable=False, unique=True)
    # Hashed password
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile info
    name = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))

    # Timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    # Friends Relationship
    friends = db.relationship(
        'User', 
        secondary='friendships',
        primaryjoin="User.id==friendships.c.user_id",
        secondaryjoin="User.id==friendships.c.friend_id",
        backref="friended_by"
    )

    def add_friend(self, user):
        if not self.is_friend(user):
            self.friends.append(user)
            user.friends.append(self)

    def remove_friend(self, user):
        if self.is_friend(user):
            self.friends.remove(user)
            user.friends.remove(self)

    def is_friend(self, user):
        return user in self.friends

    # ---------- PASSWORD HANDLING ----------
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # ---------- REPRESENTATION ----------
    def __repr__(self):
        return f"<User {self.email}>"


# Association Table
friendships = db.Table('friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)