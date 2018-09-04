from flask import current_app as app
from flask import request
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Status
from connexion import NoContent

def get_status(limit, message_type=None):
    status = Status.query.order_by(Status.id.desc())
    if message_type:
        status = status.filter(Status.message_type==message_type)
    return [s.dump() for s in status.all()][:limit]

def put_status(status):
    app.logger.info('Add status message "%s" ..', status['message'])
    status = Status(message=status['message'])
    db.session.add(status)
    db.session.commit()
    return NoContent, 200

def delete_status(status_id):
    status = Status.query.filter_by(id=status_id).first()
    if status is not None:
        app.logger.info('Deleting status message with id=%s ..', status_id)
        db.session.delete(status)
        db.session.commit()
        return NoContent, 204
    else:
        return NoContent, 404
