from sqlalchemy.sql.expression import true
from . import db
from flask_login import UserMixin,current_user
from functools import wraps
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import event
from werkzeug.security import generate_password_hash


class game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barang = db.Column(db.String(45), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Historygame(db.Model):
    __tablename__ = "historygame"
    id = db.Column(db.Integer, primary_key=True)
    id_barang = db.Column(db.Integer, db.ForeignKey('products.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(150))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default ='0')
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(64), default='customer')

    def __repr__(self) -> str:
        return '<User %s>' % self.username

class HistoryUser(db.Model, UserMixin):
    __tablename__ = "historyuser"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    action = db.Column(db.String(20))

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=true), default=func.now())
    nama_user = db.Column(db.String(150))
    message = db.Column(db.String(200))

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # Redirect the user to an unauthorized notice!
                return "You are not authorized to access this page"
            return f(*args, **kwargs)
        return wrapped
    return wrapper

