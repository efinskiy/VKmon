from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100))
    password = db.Column(db.String(300))
    is_admin = db.Column(db.Boolean)
    permission_add_new = db.Column(db.Boolean)
    permission_read_others = db.Column(db.Boolean)
    client = db.relationship('Client', backref='user')

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    vkid = db.Column(db.String(100))
    tracking_enabled = db.Column(db.Boolean)
    create_time = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    pid = db.Column(db.Integer)
    client = db.relationship('Tracking', backref='client')

class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100))
    value = db.Column(db.String(100))

class Tracking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.Integer, db.ForeignKey(Client.id))
    date_from = db.Column(db.DateTime)
    date_to = db.Column(db.DateTime)
    status = db.Column(db.Boolean)