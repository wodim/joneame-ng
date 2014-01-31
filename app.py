from flask import Flask
from werkzeug.contrib.profiler import ProfilerMiddleware

from joneame.config import _cfg
from joneame.database import db

from joneame.views import *

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = _cfg('database', 'uri')
app.config['SQLALCHEMY_ECHO'] = True
app.config['PROFILE'] = True

app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])

db.app = app
db.init_app(app)

UserView.register(app)
LinkView.register(app)
LinkListView.register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55500)
