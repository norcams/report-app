from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Status

INSTANCE = {
    'demo': {
        'name':     'demo-api-instance',
        'ip':       '127.0.0.1',
        'uptime':   10,
        'updates':  2
    }
}

def list_instances():
    return [INSTANCE[key] for key in sorted(INSTANCE.keys())]

def add_instance_report(instance):
    app.logger.debug('report acccepted %s', instance)
    return 'report added for %s' % instance['ip'], 201
