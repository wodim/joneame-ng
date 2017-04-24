from flask import Flask
from flask_babel import Babel
from werkzeug.contrib.profiler import ProfilerMiddleware
from sqltap.wsgi import SQLTapMiddleware

from joneame.config import _cfg
from joneame.database import db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = _cfg('database', 'uri')
#app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['PROFILE'] = True

app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[10])
app.wsgi_app = SQLTapMiddleware(app.wsgi_app)

#app.jinja_env.trim_blocks = True
#app.jinja_env.lstrip_blocks = True

babel = Babel(app)

db.app = app
db.init_app(app)

import joneame.views

"""
@app.context_processor
def inject():
    return {
        'random_quote': random_quote,
    }
"""
