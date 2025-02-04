import datetime
from sqlalchemy.dialects.mysql import SET
from sqlalchemy import literal

# use db object from api (not advised to use more than one db per app)
from api.models import db

class Tokens(db.Model):
    # pylint: disable=R0903
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token_hash = db.Column(db.String(63))
    name = db.Column(db.String(127))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    scope = db.Column(SET('admin', 'read'), server_default=literal('read'))

    def __repr__(self):
        return f'<Token {self.name}>'
