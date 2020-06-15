
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'NREC report api',
    'author': 'Raymond Kristiansen',
    'url': 'https://github.com/norcams/report-app',
    'download_url': 'https://github.com/norcams/report-app',
    'author_email': 'raymond.Kristiansen@uib.no',
    'version': '1.4',
    'install_requires': [
        'flask==1.1.2',
        'connexion[swagger-ui]==2.7.0',
        'Flask-SQLAlchemy==2.4.3',
        'bcrypt',
        'PyMySQL',
        'Flask-Cors',
        'mod-wsgi'
    ],
    'packages': ['api', 'oauth'],
    'scripts': [],
    'name': 'report-api',
    'options': {"bdist_wheel": {"universal": "1"}},
}

setup(**config)
