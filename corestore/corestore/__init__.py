from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['DEBUG'] = True
app.config['DB_PATH'] = './database.db'

import corestore.views as views
import corestore.corewar as corewar
