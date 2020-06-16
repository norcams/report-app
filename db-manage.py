#!/usr/bin/env python

""" Manage db tables """

from flask import Flask
from api.models import db as api
from oauth.models import db as oauth
import argparse
import sys

app = Flask(__name__)
app.config.from_pyfile('/etc/himlar/production.cfg')

actions = ['create', 'drop']

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(title='action', dest='action')
subparser.required = True

for action in actions:
    a = subparser.add_parser(action)
    a.set_defaults(action=action)
    a.add_argument('name', metavar='dbname')

options = parser.parse_args()

def action_drop():
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
    with app.app_context():
        if options.name == 'oauth':
            oauth.init_app(app)
            oauth.create_all()
            print('oauth tables created')
        if options.name == 'api':
            api.init_app(app)
            api.create_all()
            print('api tables created')

# Run local function with the same name as the action (Note: - => _)
action = locals().get('action_' + options.action.replace('-', '_'))
if not action:
    print("Function action_%s not implemented" % options.action)
    sys.exit(1)
action()
