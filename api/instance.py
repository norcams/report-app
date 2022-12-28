from flask import current_app as app
from .models import db
from .models import Instance
from .models import Owner
from connexion import NoContent
from flask import request
import datetime

def get_instances(limit, org=None):
    queries = [Owner.ip == Instance.ip]
    if org:
        queries.append(Owner.organization == org)
    instances = db.session.query(Owner, Instance).filter(*queries). \
        order_by(Instance.timestamp.asc())
    if instances.first():
        return [s.Owner.join(s.Instance.dump()) for s in instances.all()][:limit], 200
    else:
        return NoContent, 204

def get_instance(ip):
    instance = Owner.query.filter_by(ip=ip).first()
    if instance:
        app.logger.info('instance owner found {}'.format(instance.ip))
        return instance.dump()
    return NoContent, 404

def put_instance():
    instance = request.json
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
