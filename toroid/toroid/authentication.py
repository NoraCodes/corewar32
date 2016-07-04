# Database operations for CoreStore
from flask import session
from toroid import app


def check_password(password):
    ' Check a password to see if it matches the configured admin password. '
    return (password == app.config['ADMIN_PASSWORD'])


def is_authenticated():
    ' Check whether or not the session is authentcated. '
    return session.get('auth', False)


def login():
    ' Authenticate the session. '
    session['auth'] = True


def logout():
    ' De-authenticate the session. '
    session['auth'] = False
