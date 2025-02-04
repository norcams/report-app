import os
import json
import yaml
import socket
from flask import Blueprint
from flask import request
from flask import Response
from flask import current_app as app
from flask import render_template
from api.models import db as api_db
from sqlalchemy import text

simple_pages = Blueprint('pages', 'app')

@simple_pages.route("/health")
def health():
    version = 'version.yaml'
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, version)
    with open(abs_file_path, 'r') as stream:
        try:
            output = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            output = dict()
    # check db health
    try:
        with api_db.engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        code = 200
        output['database'] = 'ok'
    except Exception as e:
        app.logger.warning(e)
        output['database'] = 'error'
        code = 503
    if request.headers.get("X-Forwarded-For"):
        output['remote_addr'] = request.headers.get("X-Forwarded-For")
    else:
        output['remote_addr'] = request.remote_addr
    output['host'] = socket.gethostname()
    msg = json.dumps(output, sort_keys=True, indent=4)
    return Response(msg, mimetype='text/json', status=code)

@simple_pages.route("/")
def frontpage():
    return render_template("index.html")
    # output = "<h2>NREC report rest API server</h2>"
    # output += '<ul><li><a href=/api/v1/docs>report api v1 docs</a></li>'
    # output += '<li><a href=/oauth2/docs>oauth docs</a></li></ul>'
    # return output
