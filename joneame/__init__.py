from flask import Flask
from flask_babel import Babel

from joneame.config import _cfg
from joneame.database import db
from joneame.utils import format_dt


# initialise the app
app = Flask(__name__)

# initialise the db
app.config['SQLALCHEMY_DATABASE_URI'] = _cfg('database', 'uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# trim and strip the resulting html
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.jinja_env.filters['format_dt'] = format_dt

# initialise i18n
babel = Babel(app)

# load all views
import joneame.views
