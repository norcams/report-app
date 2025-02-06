import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-eggs'
from app import api_app
from a2wsgi import ASGIMiddleware

application = ASGIMiddleware(api_app)
