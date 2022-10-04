"""
postgresql table end example
def __init__(self, Field1_name,Field1_name,Field1_name):
        self.field1_name = field1_name
        self.field2_name = field2_name
        self.field3_name = field3_name

    def __repr__(self):
        return f"<statement>"

Consider splitting up some objects cos some of these are fucking massive

"""

from flask_login import UserMixin
from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (ARRAY, Boolean, Column, Date, DateTime, ForeignKey,
                        Integer, String, UnicodeText, create_engine)
from sqlalchemy.orm import backref, declarative_base, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .sqlite import Base


class UserRoles(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    role_name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(UnicodeText)


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    identity = Column(String(255), unique=True, nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    @property
    def password(self):
        raise AttributeError("No Reading Passwords.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, id, email, password_hash, first_name, last_name, part_of_supplier_id):
        super().__init__()
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.part_of_supplier_id = part_of_supplier_id

    def __repr__(self):
        return f"Internal User {self.id} - Email: {self.email}"
