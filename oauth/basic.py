import bcrypt
from flask import current_app as app
from connexion import request
from .models import Tokens

def get_tokeninfo():
    try:
        _, access_token = request.headers['Authorization'].split()
    except KeyError:
        access_token = ''

    auth_user = None
    if access_token:
        # This will be slow with many users...
        users = Tokens.query.order_by(Tokens.id).all()
        for user in users:
            if bcrypt.checkpw(access_token.encode('utf8'), user.token_hash.encode('utf8')):
                auth_user = user
                app.logger.debug(f'user authentication for {user.name}')
                break

    if not auth_user:
        app.logger.debug('authentication failed')
        return 'No such bearer token', 401
    return {'uid': auth_user.name, 'scope': list(auth_user.scope)}, 200

def dialog(state, client_id, response_type, redirect_uri, scope):
    #pylint: disable=W0613
    return 'Not implemented', 200

def token():
    return 'Not implemented', 200
