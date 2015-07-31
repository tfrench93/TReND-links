import datetime
from app import app
from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase(None)

class User(UserMixin, Model):
    email = CharField(unique=True)
    nickname = CharField(unique=True, null=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, email, password, admin=False):
        try:
            cls.create(
                email=email,
                password=generate_password_hash(password),
                is_admin=admin
            )
        except IntegrityError:
            raise ValueError('User already exists')

class UserProfile(Model):
    user = ForeignKeyField(User, related_name='profile')
    name = CharField(max_length=50)
    birthdate = DateField()
    country = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user_profile(cls, user, name, birthdate, country):
        try:
            cls.create(
                user=user,
                name=name,
                birthdate=birthdate,
                country=country
            )
        except IntegrityError:
            raise ValueError('Profile already exists for this user')

