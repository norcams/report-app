import os
from connexion.options import SwaggerUIOptions
from flask_cors import CORS

# requests will not use the default distro ca-bundle (with our own ca added)
os.environ['REQUESTS_CA_BUNDLE'] = '/etc/pki/tls/certs/ca-bundle.crt'

# config swagger
options = SwaggerUIOptions(
    swagger_ui_path="/docs",
    swagger_ui_config={ 'persistAuthorization': 'true'})

def load_config(app):
    # See if development config exists
    if os.path.exists("./production.cfg"):
        app.config.from_pyfile('production.cfg')
    else:
        # Production server config
        app.config.from_pyfile('/etc/himlar/production.cfg')

    cors = CORS(app, resources={r"/api/v1/status*": {"origins": "*"}})

    # This will set the need env TOKENINFO_URL from production.cfg
    token_url = app.config.get('TOKENINFO_URL')
    if token_url:
        os.environ['TOKENINFO_URL'] = token_url
        app.logger.debug(f'TOKENINFO_URL={token_url}')
