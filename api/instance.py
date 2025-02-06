import datetime
from flask import request
from flask import current_app as app
from connexion import NoContent
from .models import db
from .models import Instance
from .models import Owner

def get_instances(limit, org=None):
    queries = [Owner.ip == Instance.ip]
    if org:
        queries.append(Owner.organization == org)
    instances = db.session.query(Owner, Instance).filter(*queries). \
        order_by(Instance.last_script_run.asc())
    if instances.first():
        return [s.Owner.join(s.Instance.dump()) for s in instances.all()][:limit], 200
    return NoContent, 204

def get_instance(ip):
    instance = Owner.query.filter_by(ip=ip).first()
    if instance:
        app.logger.info(f'instance owner found {instance.ip}')
        return instance.dump()
    return NoContent, 404

def put_instance():
    instance = request.json
    i = Instance.query.filter_by(ip=instance['ip']).first()
    if i is not None:
        app.logger.info('Updating instance with ip %s ..', instance['ip'])
        instance['last_script_run'] = datetime.datetime.now()
        i.update(instance)
    else:
        app.logger.info('Creating instance with ip %s ..', instance['ip'])
        db.session.add(Instance(**instance))
    db.session.commit()
    return NoContent, (200 if i is not None else 201)
