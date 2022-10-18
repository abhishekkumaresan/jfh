from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from .utils import hash_password


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password_hash = db.Column(db.String(1000))
    email = db.Column(db.String(400))

    def __init__(self, user_name, first_name, last_name, password, email):

        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = hash_password(password)

    def __repr__(self):
        return f"{self.user_name}:{self.id}"

    @classmethod
    def is_existing(cls, user_obj):
        return cls.query.filter(
            or_(User.email == user_obj.email, User.user_name == user_obj.user_name)
        ).first()

    @classmethod
    def find_by_user_name(cls, user_name):
        return cls.query.filter_by(user_name=user_name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class Search(db.Model):
    __tablename__ = "search"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), db.ForeignKey("user.user_name"))
    search_city = db.Column(db.String(500))
    observation_time = db.Column(db.TIMESTAMP())
    weather = db.Column(db.String(20))
    temperature_celicius = db.Column(db.Float())
    temperature_celicius_indoor = db.Column(db.Float())
    humidity = db.Column(db.Float())
    humidity_indoor = db.Column(db.Float())


    @classmethod
    def find_by_user_name(cls, user_name):
        return cls.query.filter_by(user_name=user_name)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
