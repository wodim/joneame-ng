from flask import Flask
from flask_babel import Babel
from jinja2 import FileSystemBytecodeCache, StrictUndefined

from joneame.config import _cfg, _cfgb64
from joneame.database import db
from joneame.utils import format_dt, format_post_text


# initialise the app
app = Flask(__name__)
app.config['SECRET_KEY'] = _cfgb64('misc', 'secret_key')

# initialise the db
app.config['SQLALCHEMY_DATABASE_URI'] = _cfg('database', 'uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# trim and strip the resulting html
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.jinja_env.undefined = StrictUndefined

app.jinja_env.filters['format_dt'] = format_dt
app.jinja_env.filters['user_text'] = format_post_text

# jinja2 cache
bcc = FileSystemBytecodeCache('/tmp', 'jinja_jnm_%s.cache')
app.jinja_env.bytecode_cache = bcc

# initialise i18n
babel = Babel(app)

# initialise the login manager
import joneame.login

# load all views
import joneame.views
