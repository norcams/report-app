import os
import connexion
from flask import request
from api.models import db as api_db
from oauth.models import db as oauth_db

app = connexion.App(__name__, specification_dir='./')

# Production server config
app.app.config.from_pyfile('/etc/himlar/production.cfg')

# This will set the need env TOKENINFO_URL from production.cfg
token_url = app.app.config.get('TOKENINFO_URL')
if token_url:
    os.environ['TOKENINFO_URL'] = token_url

# Read the api.yaml file to configure the endpoints
app.add_api('api/api.yaml', strict_validation=True)
app.add_api('oauth/oauth2.yaml', strict_validation=True)

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

if __name__ == '__main__':
    host = app.app.config.get('HOST', '0.0.0.0')
    debug = app.app.config.get('DEBUG', False)
    port = app.app.config.get('PORT', 5000)
    app.run(host=host, port=port, debug=debug)
