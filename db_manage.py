#!/usr/bin/env python

""" Manage db tables """
import argparse
import sys
import os
from flask import Flask
from api.models import db as api
from oauth.models import db as oauth

from alembic.config import Config
from alembic import command

app = Flask(__name__)

# See if development config exists
if os.path.exists("production.cfg"):
    app.config.from_pyfile('production.cfg')
else:
    # Production server config
    app.config.from_pyfile('/etc/himlar/production.cfg')

actions = ['create', 'drop']

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(title='action', dest='action')
subparser.required = True

for action in actions:
    a = subparser.add_parser(action)
    a.set_defaults(action=action)
    a.add_argument('name', metavar='dbname', help='oauth or api')

options = parser.parse_args()

def action_drop():
    """ Drop table """
    with app.app_context():
        if options.name == 'oauth':
            oauth.init_app(app)
            oauth.drop_all()
            print('oauth tables dropped')
        if options.name == 'api':
            api.init_app(app)
            api.drop_all()
            print('api tables dropped')

def action_create():
    """ Create table """
    with app.app_context():
        if options.name == 'oauth':
            oauth.init_app(app)
            oauth.create_all()
            print('oauth tables created')
        if options.name == 'api':
            api.init_app(app)
            api.create_all()
            print('api tables created')
    # load the Alembic configuration and generate the
    # "stamping" it with the most recent rev:
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg, "head")

# Run local function with the same name as the action (Note: - => _)
action = locals().get('action_' + options.action.replace('-', '_'))
if not action:
    print(f"Function action_{options.action} not implemented")
    sys.exit(1)
action()
