import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Status(db.Model):
    __message_types = ['info', 'important']
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    message_type = db.Column(db.Enum(*__message_types), server_default='info')
    message = db.Column(db.Text,  nullable=False)

    def __repr__(self):
        return '<Status %r>' % self.id

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


class Instance(db.Model):
    __tablename__ = 'instances'
    ip = db.Column(db.String(12), primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    kernel = db.Column(db.String(127))
    md5sum = db.Column(db.String(32))
    updates = db.Column(db.Integer, nullable=False)
    uptime = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Instance %r>' % self.ip

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])

    def update(self, attributes):
        for k,v in attributes.iteritems():
            setattr(self, k, v)
