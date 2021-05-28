
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
        'SQLAlchemy<1.4',
        'flask==1.1.2',
        'connexion[swagger-ui]==2.7.0',
        'Flask-SQLAlchemy==2.5.1',
        'pytz',
        'bcrypt',
        'PyMySQL',
        'Flask-Cors',
        'mod-wsgi',
        'feedgen',
        'tabulate'
    ],
    'packages': ['api', 'oauth'],
    'scripts': [],
    'name': 'report-api',
    'options': {"bdist_wheel": {"universal": "1"}},
}

setup(**config)
