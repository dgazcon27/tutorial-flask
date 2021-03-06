from flask import url_for
from flask_login import UserMixin
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from run import db


users = []

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # def __init__(self, id, name, email, password, is_admin=False):
    #     self.id = id
    #     self.name = name
    #     self.email = email
    #     self.password = generate_password_hash(password)
    #     self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_user(email):
        for user in users:
            if user.email == email:
                return user
        return None
        
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
