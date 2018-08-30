import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import SET
from sqlalchemy import literal

db = SQLAlchemy()

class Tokens(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token_hash = db.Column(db.String(63))
    name = db.Column(db.String(127))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    scope = db.Column(SET('admin', 'read'), server_default=literal('read'))

    def __repr__(self):
        return '<Token %r>' % self.token
