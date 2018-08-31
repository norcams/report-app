from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Instance
from connexion import NoContent
import datetime

def get_instances(limit):
    instances = Instance.query.order_by(Instance.timestamp.desc())
    return [s.dump() for s in instances.all()][:limit]

def put_instance(instance):
    i = db.session.query(Instance).filter(Instance.ip == instance['ip']).one_or_none()
    #i = Instance.query().filter(Instance.ip == instance['ip']).one_or_none()
    if i is not None:
        app.logger.info('Updating instance with ip %s..', instance['ip'])
        instance['timestamp'] = datetime.datetime.now()
        #db.update(Instance).where(Instance.ip == instance['ip']).values(**instance)
        i.update(instance)
    else:
        app.logger.info('Creating instance with ip %s..', instance['ip'])
        db.session.add(Instance(**instance))
    db.session.commit()
    return NoContent, (200 if i is not None else 201)
