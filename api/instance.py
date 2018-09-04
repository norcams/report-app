from flask import current_app as app
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Instance
from models import Owner
from connexion import NoContent
import datetime
import json

def get_instances(limit, org=None):
    queries = [Owner.ip == Instance.ip]
    if org:
        queries.append(Owner.organization == org)
    instances = db.session.query(Owner, Instance).filter(*queries). \
        order_by(Instance.timestamp.asc())
    return [s.Owner.join(s.Instance.dump()) for s in instances.all()][:limit]

def put_instance(instance):
    i = Instance.query.filter_by(ip=instance['ip']).first()
    if i is not None:
        app.logger.info('Updating instance with ip %s ..', instance['ip'])
        instance['timestamp'] = datetime.datetime.now()
        i.update(instance)
    else:
        app.logger.info('Creating instance with ip %s ..', instance['ip'])
        db.session.add(Instance(**instance))
    db.session.commit()
    return NoContent, (200 if i is not None else 201)
