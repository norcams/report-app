from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class ApiModel(DeclarativeBase):
    """ Model class for all our models.
        This will included shared functions. """

    # def keys(self):
    #     return dict([k for k, v in vars(self).items() if not k.startswith('_')])

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])

    def join(self, obj):
        dump = self.dump()
        dump.update(obj)
        return dump

    def update(self, attributes):
        for k, v in attributes.items():
            setattr(self, k, v)

# Make user we use our model class
db = SQLAlchemy(model_class=ApiModel)

class Status(db.Model):
    # pylint: disable=E1101,R0903
    __message_types = ['info', 'important', 'event']
    __tablename__ = 'status'
    __table_args__ = {'mysql_engine':'InnoDB'}

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    message_type = db.Column(db.Enum(*__message_types), server_default='info')
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Status %r>' % self.id

class Instance(db.Model):
    # pylint: disable=E1101,R0903
    __tablename__ = 'instances'
    __table_args__ = {'mysql_engine':'InnoDB'}

    ip = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    kernel = db.Column(db.String(255))
    md5sum = db.Column(db.String(32))
    updates = db.Column(db.Integer, nullable=False)
    uptime = db.Column(db.Integer, nullable=False)
    last_script_run = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return '<Instance %r>' % self.ip

class Owner(db.Model):
    # pylint: disable=E1101,R0903
    __tablename__ = 'owners'
    __table_args__ = {'mysql_engine':'InnoDB'}

    ip = db.Column(db.String(16), primary_key=True)
    organization = db.Column(db.String(16), nullable=False)
    project_name = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.String(255))
    user = db.Column(db.String(255))
    last_sync = db.Column(db.DateTime, default=datetime.now, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    instance_id = db.Column(db.String(63))
    status = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return '<Owner %r>' % self.project_name
