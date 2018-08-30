import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    message = db.Column(db.Text)

    def __repr__(self):
        return '<Status %r>' % self.id
