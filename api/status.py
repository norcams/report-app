from datetime import datetime, timedelta
import pytz
from connexion import NoContent
from flask import current_app as app
from flask import request
from feedgen.feed import FeedGenerator
from .models import db
from .models import Status


def get_status(limit, limit_days, message_type=None):
    """ Get list of messages limited by number or days
        limit
    """
    start_at = datetime.today() - timedelta(days=limit_days + 1)
    app.logger.info(f'Start at set to {start_at}')
    status = Status.query.filter(Status.timestamp >= start_at).order_by(Status.id.desc())
    if message_type:
        status = status.filter(Status.message_type == message_type)
    return [s.dump() for s in status.all()][:limit]

def put_status():
    # pylint: disable=E1101
    status = request.json
    app.logger.info('Add status message "%s" ..', status['message'])
    message_type = status.get('message_type', None)
    status = Status(message=status['message'], message_type=message_type)
    db.session.add(status)
    db.session.commit()
    return NoContent, 201

def delete_status(status_id):
    # pylint: disable=E1101
    status = Status.query.filter_by(id=status_id).first()
    if status is not None:
        app.logger.info('Deleting status message with id=%s ..', status_id)
        db.session.delete(status)
        db.session.commit()
        return NoContent, 204
    return NoContent, 404

def get_rss(limit, limit_days, message_type=None):
    start_at = datetime.today() - timedelta(days=limit_days + 1)
    app.logger.info(f'get_rss: Start set to {start_at}')
    status = Status.query.filter(Status.timestamp >= start_at).order_by(Status.id.desc())
    if message_type:
        status = status.filter(Status.message_type == message_type)

    fg = FeedGenerator()
    fg.title('NREC Status updates')
    fg.language('en')
    fg.link(href='https://status.nrec.no', length=140)
    fg.description('Status messages from NREC')
    fg.docs('https://report.nrec.no/api/ui/')
    tz = pytz.timezone('Europe/Oslo')
    for s in status.all()[:limit]:
        app.logger.info(f"add {s.id}")
        fe = fg.add_entry(order='append')
        fe.id(str(s.id))
        fe.title(s.timestamp.strftime("%a, %d %b %Y"))
        fe.content(s.message)
        fe.category(category=dict({'term': s.message_type}))
        fe.published(tz.localize(s.timestamp))

    return fg.rss_str(pretty=True), 200
