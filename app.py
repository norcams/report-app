import pages
import config as config
from connexion import FlaskApp
from api.models import db

api_app = FlaskApp(__name__)

config.load_config(api_app.app)
api_app.app.register_blueprint(pages.simple_pages)
db.init_app(api_app.app)

# Read the yaml file to configure the endpoints
api_app.add_api('api/openapi-v1.yaml', base_path='/api/v1', swagger_ui_options=config.options,
            strict_validation=True, validate_responses=True)

api_app.add_api('oauth/openapi.yaml', base_path='/oauth2', swagger_ui_options=config.options,
            strict_validation=True, validate_responses=True)

@api_app.app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
    api_app.app.logger.debug('close db session')

# this is only used for running in standalone cli development mode
if __name__ == '__main__':
    host = api_app.app.config.get('HOST', '0.0.0.0')
    log_level = api_app.app.config.get('LOG_LEVEL', 'info') # only uvicorn level
    port = api_app.app.config.get('PORT', 5000)
    api_app.run("app:api_app", host=host, log_level=log_level, port=int(port), reload=True)
