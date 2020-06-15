from connexion import NoContent
from flask import current_app as app
from datetime import datetime, timedelta
from .models import db
from .models import Status

def get_status(limit, limit_days, message_type=None):
    start_at = datetime.today() - timedelta(days=limit_days + 1)
    app.logger.info('Start at set to {}'.format(start_at))
    status = Status.query.filter(Status.timestamp >= start_at).order_by(Status.id.desc())
    if message_type:
        status = status.filter(Status.message_type == message_type)
    return [s.dump() for s in status.all()][:limit]

def put_status(status):
    app.logger.info('Add status message "%s" ..', status['message'])
    message_type = status.get('message_type', None)
    status = Status(message=status['message'], message_type=message_type)
    db.session.add(status)
    db.session.commit()
    return NoContent, 201

def delete_status(status_id):
    status = Status.query.filter_by(id=status_id).first()
    if status is not None:
        app.logger.info('Deleting status message with id=%s ..', status_id)
        db.session.delete(status)
        db.session.commit()
        return NoContent, 204
    return NoContent, 404
