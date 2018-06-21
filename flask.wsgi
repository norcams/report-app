import os
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/httpd/python-eggs'
from app import app as application

