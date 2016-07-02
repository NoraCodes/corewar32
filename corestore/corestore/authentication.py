# Database operations for CoreStore
from corestore import app


def check_password(password):
    return (password == app.config['ADMIN_PASSWORD'])
