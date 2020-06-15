#!/usr/bin/env python

""" Manage oauth tokens """

import sys
import random
import string
import bcrypt
from flask import Flask
from oauth.models import db
from oauth.models import Tokens
from sqlalchemy import literal
import argparse

app = Flask(__name__)
app.config.from_pyfile('/etc/himlar/production.cfg')

actions = ['create', 'delete']

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(title='action')
for action in actions:
    a = subparser.add_parser(action)
    a.set_defaults(action=action)
    a.add_argument('name', metavar='username')
    if action == 'create':
        a.add_argument('scope', metavar='scope', nargs='+', default='read')
options = parser.parse_args()

def action_create():
    with app.app_context():
        db.init_app(app)
        chars = string.ascii_letters + string.digits
        token = ''.join(random.choice(chars) for _ in range(32))
        token_hash = bcrypt.hashpw(token, bcrypt.gensalt())
        scope = literal(','.join(options.scope))
        db.session.add(Tokens(token_hash=token_hash, name=options.name, scope=scope))
        db.session.commit()
        print('token: {} with scope {}'.format(token, ','.join(options.scope)))

def action_delete():
    with app.app_context():
        db.init_app(app)
        users = Tokens.query.filter_by(name=options.name).all()
        for u in users:
            db.session.delete(u)
        db.session.commit()
        print('delete all users with name {}'.format(options.name))


# Run local function with the same name as the action (Note: - => _)
action = locals().get('action_' + options.action.replace('-', '_'))
if not action:
    print("Function action_%s not implemented" % options.action)
    sys.exit(1)
action()
