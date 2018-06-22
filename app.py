import connexion
from flask import request

app = connexion.App(__name__, specification_dir='./')

# Production server config
app.app.config.from_pyfile('production.cfg')

# Read the api.yml file to configure the endpoints
app.add_api('report-api/api.yaml', strict_validation=True)

# Default landing page
@app.route("/")
def docs():
    print type(request)
    return '<a href=' + request.base_url + 'api/ui' + '>report api docs</a>'

if __name__ == '__main__':
    host = app.app.config.get('HOST', '0.0.0.0')
    debug = app.app.config.get('DEBUG', False)
    port = app.app.config.get('PORT', 5000)
    app.run(host=host, port=port, debug=debug)
