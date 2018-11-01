import os
import json
import socket
import connexion
import yaml
import pymysql
from flask_cors import CORS
from flask import request
from flask import Response
from api.models import db as api_db
from oauth.models import db as oauth_db

app = connexion.App(__name__, specification_dir='./')

cors = CORS(app.app, resources={r"/api/v1/status*": {"origins": "*"}})

# Production server config
app.app.config.from_pyfile('/etc/himlar/production.cfg')

# This will set the need env TOKENINFO_URL from production.cfg
token_url = app.app.config.get('TOKENINFO_URL')
if token_url:
    os.environ['TOKENINFO_URL'] = token_url

# requests will not use the default distro ca-bundle (with our own ca added)
os.environ['REQUESTS_CA_BUNDLE'] = '/etc/pki/tls/certs/ca-bundle.crt'

# Read the api.yaml file to configure the endpoints
app.add_api('api/api.yaml', strict_validation=True, validate_responses=False)
app.add_api('oauth/oauth2.yaml', strict_validation=True, validate_responses=True)

# Database setup - this will make import db work inside packages without more sql config
oauth_db.init_app(app.app)
api_db.init_app(app.app)

# Default landing page
@app.route("/")
def docs():
    output = "<h2>UH-IaaS report rest API server</h2>"
    output += '<ul><li><a href=' + request.base_url + 'api/ui' + '>report api docs</a></li>'
    output += '<li><a href=' + request.base_url + 'oauth2/ui' + '>oauth docs</a></li></ul>'
    return output

@app.route("/health")
def health():
    version = 'version.yaml'
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, version)
    with open(abs_file_path, 'r') as stream:
        try:
            output = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            output = dict()
    # check db health
    try:
        api_db.engine.execute('SELECT 1')
        code = 200
        output['database'] = 'ok'
    except Exception as e:
        output['database'] = 'error'
        code = 503
    if request.headers.get("X-Forwarded-For"):
        output['remote_addr'] = request.headers.get("X-Forwarded-For")
    else:
        output['remote_addr'] = request.remote_addr
    output['host'] = socket.gethostname()
    msg = json.dumps(output, sort_keys=True, indent=4)
    return Response(msg, mimetype='text/json', status=code)

@app.app.teardown_appcontext
def shutdown_session(exception=None):
    oauth_db.session.remove()
    api_db.session.remove()
    app.app.logger.debug('close db session')

if __name__ == '__main__':
    host = app.app.config.get('HOST', '0.0.0.0')
    debug = app.app.config.get('DEBUG', False)
    port = app.app.config.get('PORT', 5000)
    app.run(host=host, port=port, debug=debug)
